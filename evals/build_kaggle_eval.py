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
    "dev-valid-training-gold-scorable-54": ROOT / "evals" / "dev-valid-training-gold-scorable-54-task-ids.json",
    "dev-valid-training-wheelhouse-qualified-53": ROOT / "evals" / "dev-valid-training-wheelhouse-qualified-53-task-ids.json",
    "patch-completion-screen": ROOT / "evals" / "patch-completion-screen-task-ids.json",
    "issue-localization-rich-pair": ROOT / "evals" / "issue-localization-rich-pair-task-ids.json",
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


def _agent_spec(agent: str, model: str, seed: int) -> dict:
    agent_dir = AGENTS_DIR / agent
    if not agent_dir.is_dir() or agent.startswith("reference-"):
        raise ValueError(f"Unknown tracked agent: {agent}")
    files = _agent_files(agent_dir, model)
    _set_request_seed(files, seed)
    return {
        "agent": agent,
        "files": files,
        "max_tool_calls": _eval_config_value(files, "max_tool_calls", 40),
        "max_time_minutes": _eval_config_value(files, "max_time_minutes", 8.0),
    }


def build_notebook(
    agent: str | list[str],
    model: str,
    task_set: str | list[str],
    output_dir: Path,
    kernel_id: str = KERNEL_ID,
    kernel_title: str = KERNEL_TITLE,
    seed: int = 42,
) -> tuple[Path, Path]:
    if model not in MODEL_SOURCES:
        raise ValueError(f"Unsupported competition model: {model}")

    agents = [agent] if isinstance(agent, str) else list(agent)
    if not agents:
        raise ValueError("At least one tracked agent is required")
    task_sets = [task_set] * len(agents) if isinstance(task_set, str) else list(task_set)
    if len(task_sets) != len(agents):
        raise ValueError("Provide exactly one task set for each agent")
    unknown_task_sets = [name for name in task_sets if name not in TASK_SETS]
    if unknown_task_sets:
        raise ValueError(f"Unknown task set: {unknown_task_sets[0]}")
    if len(set(agents)) != len(agents):
        raise ValueError("Agents must be unique")
    specs = [_agent_spec(name, model, seed) for name in agents]
    if len(specs) > 1:
        if len({spec["max_tool_calls"] for spec in specs}) != 1:
            raise ValueError("Run suite agents must have the same max_tool_calls")
        if len({spec["max_time_minutes"] for spec in specs}) != 1:
            raise ValueError("Run suite agents must have the same max_time_minutes")
        if len({spec["files"]["configs/sampling.yaml"] for spec in specs}) != 1:
            raise ValueError("Run suite agents must have identical sampling configuration")

    for spec, task_set_name in zip(specs, task_sets):
        spec["task_set"] = task_set_name
        spec["task_ids"] = json.loads(TASK_SETS[task_set_name].read_text(encoding="utf-8"))
    runtime = (ROOT / "evals" / "kaggle_runtime.py").read_text(encoding="utf-8")
    if len(specs) == 1:
        spec = specs[0]
        task_ids = spec["task_ids"]
        code = (
            "AGENT_FILES = " + json.dumps(spec["files"], ensure_ascii=False) + "\n"
            + "TASK_IDS = " + json.dumps(task_ids) + "\n"
            + f"MODEL_NAME = {model!r}\n"
            + f"MAX_TOOL_CALLS = {spec['max_tool_calls']}\n"
            + f"MAX_TIME_MINUTES = {spec['max_time_minutes']}\n"
            + f"REQUEST_SEED = {seed}\n"
            + "\n"
            + "RUNTIME_SOURCE = " + repr(runtime) + "\n"
            + "exec(compile(RUNTIME_SOURCE, 'kaggle_runtime.py', 'exec'))\n"
            + "run_dev_eval(AGENT_FILES, TASK_IDS, MODEL_NAME, max_tool_calls=MAX_TOOL_CALLS, max_time_minutes=MAX_TIME_MINUTES, seed=REQUEST_SEED)\n"
        )
    else:
        run_specs = [
            {
                "agent": spec["agent"],
                "task_set": spec["task_set"],
                "task_ids": spec["task_ids"],
                "agent_files": spec["files"],
                "max_tool_calls": spec["max_tool_calls"],
                "max_time_minutes": spec["max_time_minutes"],
            }
            for spec in specs
        ]
        code = (
            "RUN_SPECS = " + json.dumps(run_specs, ensure_ascii=False) + "\n"
            + f"MODEL_NAME = {model!r}\n"
            + f"REQUEST_SEED = {seed}\n"
            + "\n"
            + "RUNTIME_SOURCE = " + repr(runtime) + "\n"
            + "exec(compile(RUNTIME_SOURCE, 'kaggle_runtime.py', 'exec'))\n"
            + "for run_spec in RUN_SPECS:\n"
            + "    print(f\"AGENT_EVAL_START={run_spec['agent']} TASK_SET={run_spec['task_set']}\")\n"
            + "    run_dev_eval(\n"
            + "        run_spec['agent_files'], run_spec['task_ids'], MODEL_NAME,\n"
            + "        max_tool_calls=run_spec['max_tool_calls'],\n"
            + "        max_time_minutes=run_spec['max_time_minutes'], seed=REQUEST_SEED,\n"
            + "    )\n"
            + "    print(f\"AGENT_EVAL_DONE={run_spec['agent']} TASK_SET={run_spec['task_set']}\")\n"
        )
    run_labels = [
        f"`{spec['agent']}` on `{spec['task_set']}` ({len(spec['task_ids'])} tasks)"
        for spec in specs
    ]
    if len(specs) == 1:
        intro = (
            f"Agent: `{agents[0]}`  \nModel: `{model}`  \nTask set: `{task_sets[0]}` ({len(specs[0]['task_ids'])} tasks).  \nRequest seed: `{seed}`.\n"
            "\nRuns the official competition evaluator on training tasks. The score is a development metric, not a leaderboard estimate."
        )
    else:
        intro = (
            f"Run plan: {', '.join(run_labels)}  \nModel: `{model}`  \nRequest seed: `{seed}`.\n"
            "\nRuns each candidate sequentially in one Kaggle session with the same model, sampling configuration, and budgets. Each run starts a fresh model server to reset the request seed. Scores are development metrics, not leaderboard estimates."
        )
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "private-dev-eval-intro",
                "metadata": {},
                "source": [
                    "# Private Gemma 4 fixed-set evaluation\n",
                    "\n" + intro,
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
    parser.add_argument("--agents", choices=names, nargs="+", help="Run matched candidates sequentially in one Kaggle session")
    parser.add_argument("--model", choices=sorted(MODEL_SOURCES), default="gemma-4-31b-it-qat-w4a16-ct")
    parser.add_argument("--task-set", choices=sorted(TASK_SETS), default="smoke")
    parser.add_argument("--task-sets", choices=sorted(TASK_SETS), nargs="+", help="One task set per value in --agents")
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
    if args.task_sets and not args.agents:
        parser.error("--task-sets requires --agents")
    if args.task_sets and len(args.task_sets) != len(args.agents):
        parser.error("--task-sets must have exactly one entry per --agents value")
    task_sets = args.task_sets if args.task_sets else args.task_set
    notebook, metadata = build_notebook(
        args.agents if args.agents else args.agent,
        args.model,
        task_sets,
        args.output_dir,
        args.kernel_id,
        args.kernel_title,
        args.seed,
    )
    print(f"Generated private Kaggle kernel: {notebook}")
    print(f"Metadata: {metadata}")
    print(f"Agents: {', '.join(args.agents) if args.agents else args.agent}")
    print(f"Task sets: {', '.join(task_sets) if isinstance(task_sets, list) else task_sets}")


if __name__ == "__main__":
    main()
