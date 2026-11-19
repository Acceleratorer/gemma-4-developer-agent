"""Build a CPU-only Kaggle notebook for official-verifier gold-patch checks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_SETS = {
    "dev-valid-expanded": ROOT / "evals" / "dev-valid-expanded-task-ids.json",
    "dev-valid-unseen": ROOT / "evals" / "dev-valid-unseen-task-ids.json",
    "httpx-verifier-candidate": ROOT / "evals" / "httpx-verifier-candidate-task-ids.json",
    "fastapi-rich-issue-only-candidates": ROOT / "evals" / "fastapi-rich-issue-only-candidate-task-ids.json",
}
DOCKER_IMAGE = (
    "gcr.io/kaggle-private-byod/python@sha256:"
    "37c64f7dd9c54116ecd1bcc88817c5469b88387388fade02bfa8bf3fc647d461"
)


def _task_ids(task_set: str) -> list[str]:
    ids = json.loads(TASK_SETS[task_set].read_text(encoding="utf-8"))
    if not ids or len(ids) != len(set(ids)) or any(not re.fullmatch(r"[a-z0-9_]+", item) for item in ids):
        raise ValueError(f"Invalid or duplicate task IDs in {TASK_SETS[task_set]}")
    return ids


def build_notebook(task_set: str, output_dir: Path, kernel_id: str, kernel_title: str) -> tuple[Path, Path]:
    if task_set not in TASK_SETS:
        raise ValueError(f"Unknown task set: {task_set}")
    if not kernel_id.startswith("accelra/"):
        raise ValueError("Kernel ID must use the accelra owner")
    title_slug = re.sub(r"[^a-z0-9]+", "-", kernel_title.lower()).strip("-")
    if kernel_id.split("/", 1)[1] != title_slug:
        raise ValueError(f"Kernel ID slug must match title slug: {title_slug}")

    task_ids = _task_ids(task_set)
    runtime_source = (ROOT / "evals" / "kaggle_runtime.py").read_text(encoding="utf-8")
    code = f'''RUNTIME_SOURCE = {runtime_source!r}
exec(compile(RUNTIME_SOURCE, "kaggle_runtime.py", "exec"))

from pathlib import Path
import json, time, traceback

_configure_environment()
data_dir = Path("/kaggle/input/competitions/gemma-4-developer-agent")
_install_wheelhouse(Path("/kaggle/input/datasets/metric/gemma-4-developer-agent-wheelhouse"))
from swegemma.config import EvalConfig
from swegemma.deduplication import resolve_task_snapshot_paths
from swegemma.evaluate import Evaluator
from swegemma.harness.verification import verify_task
from swegemma.models import load_tasks

task_path = data_dir / "tasks.jsonl"
results_dir = Path("/kaggle/working/gold-patch-results")
results_dir.mkdir(parents=True, exist_ok=True)
agent_dir = Path("/kaggle/working/empty-agent")
agent_dir.mkdir(parents=True, exist_ok=True)
TASK_IDS = {task_ids!r}
eval_config = EvalConfig(
    tasks_path=task_path,
    snapshots_dir=data_dir / "snapshots",
    results_dir=results_dir,
    submission_dir=agent_dir,
    models=None,
    sandbox="subprocess",
    timeout_seconds=180,
    verification_timeout_seconds=300,
    wheels_dir=data_dir / "wheels",
    graph_dir=data_dir / "graphs",
    embeddings_dir=data_dir / "embeddings",
    verbose=False,
)
evaluator = Evaluator(eval_config)
tasks = {{task.instance_id: task for task in load_tasks(task_path)}}
rows = []
for index, task_id in enumerate(TASK_IDS, 1):
    task = tasks[task_id]
    print(f"[{{index}}/{{len(TASK_IDS)}}] {{task_id}} patch_chars={{len(task.patch)}}")
    try:
        snapshot_path, base_snapshot_path, patch_path = resolve_task_snapshot_paths(
            eval_config.snapshots_dir, task.instance_id, task.repo
        )
        if not snapshot_path.exists():
            _, _, secret_dir = evaluator._get_secret_bundle_data()
            if secret_dir is not None and (secret_dir / "sandbox" / "snapshots").is_dir():
                snapshot_path, base_snapshot_path, patch_path = resolve_task_snapshot_paths(
                    secret_dir / "sandbox" / "snapshots", task.instance_id, task.repo
                )
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {{snapshot_path}}")
        if not task.patch.strip():
            raise ValueError("Task has no public reference patch")
        started = time.perf_counter()
        result = _run_sync(
            verify_task,
            evaluator.docker,
            eval_config,
            task,
            snapshot_path,
            base_snapshot_path=base_snapshot_path,
            patch_path=patch_path,
            agent_patch=task.patch,
            start_time=started,
        )
        row = {{
            "id": task_id,
            "repo": task.repo,
            "resolved": bool(result.resolved),
            "test_exit_code": result.test_exit_code,
            "reference_patch_chars": len(task.patch),
            "duration_seconds": result.duration_seconds,
            "error": result.error,
            "test_output": (result.test_output or "")[-12000:],
        }}
    except Exception as exc:
        row = {{"id": task_id, "repo": task.repo, "resolved": False,
               "reference_patch_chars": len(task.patch), "error": repr(exc),
               "traceback": traceback.format_exc()[-12000:]}}
    rows.append(row)
    print(json.dumps(row, ensure_ascii=False))

summary = {{
    "purpose": "positive-control evaluation using each public task.patch",
    "task_ids": TASK_IDS,
    "resolved": sum(row.get("resolved", False) for row in rows),
    "total": len(rows),
    "results": rows,
}}
(results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
output_file = Path("/kaggle/working/gold-patch-summary.json")
output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"GOLD_PATCH_SCORE={{summary['resolved']}}/{{summary['total']}}")
print(f"RESULT_FILE={{output_file}}")
'''
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "gold-patch-control-intro",
                "metadata": {},
                "source": [
                    "# Gold patch verifier positive control\n\n",
                    f"Task set: `{task_set}` ({len(task_ids)} tasks).\n\n",
                    "Runs the official verifier with public reference patches. This is a verifier diagnostic, not an agent score.",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "gold-patch-control-run",
                "metadata": {},
                "outputs": [],
                "source": code.splitlines(keepends=True),
            },
        ],
        "metadata": {
            "kaggle": {"accelerator": "none", "isGpuEnabled": False, "isInternetEnabled": False},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.13"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    metadata = {
        "id": kernel_id,
        "title": kernel_title,
        "code_file": "gold_patch_eval.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": [],
        "dataset_sources": ["metric/gemma-4-developer-agent-wheelhouse"],
        "kernel_sources": [],
        "competition_sources": ["gemma-4-developer-agent"],
        "model_sources": [],
        "docker_image": DOCKER_IMAGE,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    notebook_path = output_dir / "gold_patch_eval.ipynb"
    metadata_path = output_dir / "kernel-metadata.json"
    notebook_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return notebook_path, metadata_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-set", choices=sorted(TASK_SETS), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--kernel-id", required=True)
    parser.add_argument("--kernel-title", required=True)
    args = parser.parse_args()
    notebook_path, metadata_path = build_notebook(
        args.task_set, args.output_dir, args.kernel_id, args.kernel_title
    )
    print(f"Generated CPU-only gold-patch kernel: {notebook_path}")
    print(f"Metadata: {metadata_path}")
    print(f"Tasks: {args.task_set} ({len(_task_ids(args.task_set))})")


if __name__ == "__main__":
    main()
