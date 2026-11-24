"""Compare two fixed-set evaluation summaries by task ID."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_summary(path: Path) -> dict[str, Any]:
    summary = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(summary, dict):
        raise ValueError(f"{path}: summary must be a JSON object")

    task_ids = summary.get("task_ids")
    results = summary.get("results")
    if not isinstance(task_ids, list) or not all(isinstance(task_id, str) for task_id in task_ids):
        raise ValueError(f"{path}: task_ids must be a list of strings")
    if len(task_ids) != len(set(task_ids)):
        raise ValueError(f"{path}: task_ids contains duplicates")
    if not isinstance(results, list) or not all(isinstance(result, dict) for result in results):
        raise ValueError(f"{path}: results must be a list of objects")

    result_ids = [result.get("id") for result in results]
    if not all(isinstance(result_id, str) for result_id in result_ids):
        raise ValueError(f"{path}: result IDs must be strings")
    if len(result_ids) != len(set(result_ids)) or set(result_ids) != set(task_ids):
        raise ValueError(f"{path}: result IDs do not match task_ids")
    if not all(isinstance(result.get("resolved"), bool) for result in results):
        raise ValueError(f"{path}: each result must have a boolean resolved value")
    if summary.get("total") != len(task_ids):
        raise ValueError(f"{path}: total does not match task_ids")
    if summary.get("resolved") != sum(result["resolved"] for result in results):
        raise ValueError(f"{path}: resolved does not match results")
    if not isinstance(summary.get("model"), str):
        raise ValueError(f"{path}: model is missing")
    return summary


def compare_summaries(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    if baseline["model"] != candidate["model"]:
        raise ValueError("model mismatch")
    if set(baseline["task_ids"]) != set(candidate["task_ids"]):
        raise ValueError("task-set mismatch")

    baseline_results = {result["id"]: result["resolved"] for result in baseline["results"]}
    candidate_results = {result["id"]: result["resolved"] for result in candidate["results"]}
    task_ids = baseline["task_ids"]
    gains = [task_id for task_id in task_ids if candidate_results[task_id] and not baseline_results[task_id]]
    losses = [task_id for task_id in task_ids if baseline_results[task_id] and not candidate_results[task_id]]
    shared_passes = [task_id for task_id in task_ids if baseline_results[task_id] and candidate_results[task_id]]
    shared_failures = [task_id for task_id in task_ids if not baseline_results[task_id] and not candidate_results[task_id]]

    def run_details(summary: dict[str, Any]) -> dict[str, Any]:
        durations = [result["duration_seconds"] for result in summary["results"] if isinstance(result.get("duration_seconds"), (int, float))]
        return {
            "run_id": summary.get("run_id"),
            "agent_sha256": summary.get("agent_sha256"),
            "request_seed": summary.get("request_seed"),
            "max_tool_calls": summary.get("max_tool_calls"),
            "max_time_minutes": summary.get("max_time_minutes"),
            "resolved": summary["resolved"],
            "total": summary["total"],
            "task_minutes": round(sum(durations) / 60, 2) if durations else None,
        }

    return {
        "model": baseline["model"],
        "paired_tasks": len(task_ids),
        "task_order_matches": task_ids == candidate["task_ids"],
        "baseline": run_details(baseline),
        "candidate": run_details(candidate),
        "candidate_delta": candidate["resolved"] - baseline["resolved"],
        "gains": gains,
        "losses": losses,
        "shared_passes": len(shared_passes),
        "shared_failures": len(shared_failures),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path, help="baseline summary.json")
    parser.add_argument("candidate", type=Path, help="candidate summary.json")
    args = parser.parse_args()
    try:
        report = compare_summaries(read_summary(args.baseline), read_summary(args.candidate))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
