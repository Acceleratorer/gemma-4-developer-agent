"""Generate a private Kaggle notebook for fixed-set agent evaluation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "module" / "agents"
KERNEL_ID = "accelra/gemma-4-developer-agent-evaluation"
KERNEL_TITLE = "Gemma 4 Developer Agent Evaluation"
# Match the evaluation wheelhouse's CPython 3.12 ABI instead of Kaggle's latest default image.
KAGGLE_DOCKER_IMAGE = (
    "gcr.io/kaggle-private-byod/python@sha256:37c64f7dd9c54116ecd1bcc88817c5469b88387388fade02bfa8bf3fc647d461"
)
MODEL_SOURCES = {
    "gemma-4-31b-it-qat-w4a16-ct": "google/gemma-4/Other/gemma-4-31b-it-qat-w4a16-ct/2",
    "gemma-4-12b-it-qat-w4a16-ct": "google/gemma-4/Other/gemma-4-12b-it-qat-w4a16-ct/2",
    "gemma-4-e4b-it-qat-w4a16-ct": "google/gemma-4/Other/gemma-4-e4b-it-qat-w4a16-ct/2",
    "gemma-4-e2b-it-qat-w4a16-ct": "google/gemma-4/Other/gemma-4-e2b-it-qat-w4a16-ct/2",
}
TASK_SETS = {
    "smoke": ROOT / "evals" / "smoke-task-ids.json",
    "dev": ROOT / "evals" / "dev-task-ids.json",
    "dev-valid": ROOT / "evals" / "dev-valid-task-ids.json",
    "dev-valid-crossrepo": ROOT / "evals" / "dev-valid-crossrepo-task-ids.json",
    "dev-valid-expanded": ROOT / "evals" / "dev-valid-expanded-task-ids.json",
    "dev-valid-expanded-gold-verified": ROOT / "evals" / "dev-valid-expanded-gold-verified-task-ids.json",
    "dev-valid-training-gold-verified": ROOT / "evals" / "dev-valid-training-gold-verified-task-ids.json",
    "v5-test-aware-fastapi-probe": ROOT / "evals" / "v5-test-aware-fastapi-probe-task-ids.json",
    "v5-test-aware-pilot": ROOT / "evals" / "v5-test-aware-pilot-task-ids.json",
    "dev-valid-unseen": ROOT / "evals" / "dev-valid-unseen-task-ids.json",
    "dev-valid-unseen-gold-verified": ROOT / "evals" / "dev-valid-unseen-gold-verified-task-ids.json",
}
MODEL_LINE = re.compile(r"(?m)^(\s*model:\s*)([^\s#]+)(\s*(?:#.*)?$)")


def _agent_files(agent_dir: Path, model: str) -> dict[str, str]:
    files = {}
    model_declarations = 0
    for path in sorted(agent_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Agent source cannot contain symlinks: {path}")
        if path.is_file():
            relative = path.relative_to(agent_dir).as_posix()
            content = path.read_text(encoding="utf-8")
            if path.suffix.lower() in {".yaml", ".yml"}:
                content, count = MODEL_LINE.subn(
                    lambda match: f"{match.group(1)}{model}{match.group(3)}", content
                )
                model_declarations += count
            files[relative] = content
    if model_declarations == 0:
        raise ValueError(f"No model declaration found in agent: {agent_dir}")
    return files


def _set_request_seed(agent_files: dict[str, str], seed: int) -> None:
    path = "configs/sampling.yaml"
    sampling = agent_files.get(path)
    if sampling is None:
        raise ValueError(f"Agent is missing {path}")
    matches = list(re.finditer(r"(?m)^seed\s*:.*$", sampling))
    if len(matches) > 1:
        raise ValueError(f"Agent has multiple root seed entries in {path}")
    if matches:
        sampling = re.sub(r"(?m)^seed\s*:.*$", f"seed: {seed}", sampling)
    else:
        sampling = f"seed: {seed}\n{sampling}"
    agent_files[path] = sampling


def _eval_config_value(agent_files: dict[str, str], name: str, default: int | float) -> str:
    config = agent_files.get("eval_config.yaml", "")
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*(\d+(?:\.\d+)?)\s*$", config)
    return match.group(1) if match else str(default)


def build_notebook(
    agent: str,
    model: str,
    task_set: str,
    output_dir: Path,
    kernel_id: str = KERNEL_ID,
    kernel_title: str = KERNEL_TITLE,
    seed: int = 42,
) -> tuple[Path, Path]:
    agent_dir = AGENTS_DIR / agent
    if not agent_dir.is_dir() or agent.startswith("reference-"):
        raise ValueError(f"Unknown tracked agent: {agent}")
    if model not in MODEL_SOURCES:
        raise ValueError(f"Unsupported competition model: {model}")
    if task_set not in TASK_SETS:
        raise ValueError(f"Unknown task set: {task_set}")

    agent_files = _agent_files(agent_dir, model)
    _set_request_seed(agent_files, seed)
    max_tool_calls = _eval_config_value(agent_files, "max_tool_calls", 40)
    max_time_minutes = _eval_config_value(agent_files, "max_time_minutes", 8.0)
    task_ids = json.loads(TASK_SETS[task_set].read_text(encoding="utf-8"))
    runtime = (ROOT / "evals" / "kaggle_runtime.py").read_text(encoding="utf-8")
    code = (
        "AGENT_FILES = " + json.dumps(agent_files, ensure_ascii=False) + "\n"
        + "TASK_IDS = " + json.dumps(task_ids) + "\n"
        + f"MODEL_NAME = {model!r}\n"
        + f"MAX_TOOL_CALLS = {max_tool_calls}\n"
        + f"MAX_TIME_MINUTES = {max_time_minutes}\n"
        + f"REQUEST_SEED = {seed}\n"
        + "\n"
        + "RUNTIME_SOURCE = " + repr(runtime) + "\n"
        + "exec(compile(RUNTIME_SOURCE, 'kaggle_runtime.py', 'exec'))\n"
        + "run_dev_eval(AGENT_FILES, TASK_IDS, MODEL_NAME, max_tool_calls=MAX_TOOL_CALLS, max_time_minutes=MAX_TIME_MINUTES, seed=REQUEST_SEED)\n"
    )
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "private-dev-eval-intro",
                "metadata": {},
                "source": [
                    "# Private Gemma 4 fixed-set evaluation\n",
                    f"\nAgent: `{agent}`  \nModel: `{model}`  \nTask set: `{task_set}` ({len(task_ids)} tasks).  \nRequest seed: `{seed}`.\n",
                    "\nRuns the official competition evaluator on training tasks. The score is a development metric, not a leaderboard estimate.",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "private-dev-eval-run",
                "metadata": {},
                "outputs": [],
                "source": code.splitlines(keepends=True),
            },
        ],
        "metadata": {
            "kaggle": {"accelerator": "nvidiaL4", "isGpuEnabled": True, "isInternetEnabled": False},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    metadata = {
        "id": kernel_id,
        "title": kernel_title,
        "code_file": "dev_eval.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": ["gpu"],
        "dataset_sources": ["metric/gemma-4-developer-agent-wheelhouse"],
        "kernel_sources": [],
        "competition_sources": ["gemma-4-developer-agent"],
        "model_sources": [MODEL_SOURCES[model]],
        "docker_image": KAGGLE_DOCKER_IMAGE,
        "machine_shape": "NvidiaL4",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    notebook_path = output_dir / "dev_eval.ipynb"
    metadata_path = output_dir / "kernel-metadata.json"
    notebook_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return notebook_path, metadata_path


def main() -> None:
    names = sorted(path.name for path in AGENTS_DIR.iterdir() if path.is_dir() and not path.name.startswith("reference-"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=names, default="current")
    parser.add_argument("--model", choices=sorted(MODEL_SOURCES), default="gemma-4-31b-it-qat-w4a16-ct")
    parser.add_argument("--task-set", choices=sorted(TASK_SETS), default="smoke")
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Request and vLLM seed for reproducible comparisons",
    )
    parser.add_argument("--output-dir", type=Path, default=ROOT / "evals" / "kaggle-dev-eval")
    parser.add_argument("--kernel-id", default=KERNEL_ID)
    parser.add_argument("--kernel-title", default=KERNEL_TITLE)
    args = parser.parse_args()
    notebook, metadata = build_notebook(
        args.agent,
        args.model,
        args.task_set,
        args.output_dir,
        args.kernel_id,
        args.kernel_title,
        args.seed,
    )
    print(f"Generated private Kaggle kernel: {notebook}")
    print(f"Metadata: {metadata}")
    print(f"Tasks: {args.task_set}")


if __name__ == "__main__":
    main()
