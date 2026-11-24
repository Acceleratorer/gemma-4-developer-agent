from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evals.build_kaggle_eval import build_notebook
from evals.compare_eval_summaries import compare_summaries, read_summary

ROOT = Path(__file__).resolve().parents[1]


def _task_ids(name: str) -> list[str]:
    path = ROOT / "evals" / name
    return json.loads(path.read_text(encoding="utf-8"))


class EvaluationTaskSetTests(unittest.TestCase):
    def test_wheelhouse_qualified_selection_preserves_the_unseen_holdout(self) -> None:
        training = _task_ids("dev-valid-training-gold-verified-task-ids.json")
        candidate = _task_ids("dev-valid-training-gold-scorable-54-task-ids.json")
        selection = _task_ids("dev-valid-training-wheelhouse-qualified-53-task-ids.json")
        holdout = _task_ids("dev-valid-unseen-gold-verified-task-ids.json")

        self.assertEqual(len(training), 44)
        self.assertEqual(len(candidate), 54)
        self.assertEqual(len(selection), 53)
        self.assertEqual(len(set(selection)), 53)
        self.assertEqual(selection, [task for task in candidate if task != "rich_4070"])
        self.assertIn("rich_3782", selection)
        self.assertTrue(set(training).issubset(selection))
        self.assertTrue(set(selection).isdisjoint(holdout))

    def test_issue_localization_screen_is_the_v5_ordered_training_pair(self) -> None:
        selection = _task_ids("dev-valid-training-wheelhouse-qualified-53-task-ids.json")
        screen = _task_ids("issue-localization-rich-pair-task-ids.json")

        self.assertEqual(screen, ["rich_3894", "rich_4076"])
        self.assertEqual(screen, [task for task in selection if task in set(screen)])


class KaggleEvaluationNotebookBuilderTests(unittest.TestCase):
    def test_single_agent_keeps_the_existing_notebook_flow(self) -> None:
        with TemporaryDirectory() as temp_dir:
            notebook_path, _ = build_notebook(
                "current",
                "gemma-4-31b-it-qat-w4a16-ct",
                "smoke",
                Path(temp_dir),
            )
            notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
            code = "".join(notebook["cells"][1]["source"])

        self.assertIn("AGENT_FILES = ", code)
        self.assertIn("run_dev_eval(AGENT_FILES", code)
        self.assertNotIn("RUN_SPECS = ", code)

    def test_builds_a_matched_pair_for_one_kaggle_session(self) -> None:
        with TemporaryDirectory() as temp_dir:
            notebook_path, metadata_path = build_notebook(
                ["current", "patchsmith-exp021-exact-v1"],
                "gemma-4-31b-it-qat-w4a16-ct",
                "dev-valid-training-wheelhouse-qualified-53",
                Path(temp_dir),
                kernel_id="accelra/test-paired-eval",
                kernel_title="Test Paired Eval",
                seed=42,
            )

            notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            code = "".join(notebook["cells"][1]["source"])
            intro = "".join(notebook["cells"][0]["source"])

        self.assertIn('"agent": "current"', code)
        self.assertIn('"agent": "patchsmith-exp021-exact-v1"', code)
        self.assertIn("for run_spec in RUN_SPECS:", code)
        self.assertEqual(code.count("    run_dev_eval(\n        run_spec"), 1)
        self.assertIn("fresh model server", intro)
        self.assertEqual(metadata["model_sources"], ["google/gemma-4/Other/gemma-4-31b-it-qat-w4a16-ct/2"])
        self.assertTrue(metadata["enable_gpu"])

    def test_builds_a_probe_and_paired_comparison_run_suite(self) -> None:
        with TemporaryDirectory() as temp_dir:
            notebook_path, _ = build_notebook(
                ["budget-fit-v5-validation-contract-v1", "current", "patchsmith-exp021-exact-v1"],
                "gemma-4-31b-it-qat-w4a16-ct",
                [
                    "v5-test-aware-fastapi-probe",
                    "dev-valid-training-wheelhouse-qualified-53",
                    "dev-valid-training-wheelhouse-qualified-53",
                ],
                Path(temp_dir),
                seed=42,
            )
            notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
            code = "".join(notebook["cells"][1]["source"])
            intro = "".join(notebook["cells"][0]["source"])

        self.assertIn('"task_set": "v5-test-aware-fastapi-probe"', code)
        self.assertIn('"task_set": "dev-valid-training-wheelhouse-qualified-53"', code)
        self.assertIn("run_spec['agent_files'], run_spec['task_ids'], MODEL_NAME", code)
        self.assertIn("1 tasks", intro)
        self.assertIn("53 tasks", intro)

    def test_rejects_matched_pairs_with_different_call_budgets(self) -> None:
        with TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "same max_tool_calls"):
                build_notebook(
                    ["current", "budget-fit-v5-40-calls"],
                    "gemma-4-31b-it-qat-w4a16-ct",
                    "dev-valid-training-wheelhouse-qualified-53",
                    Path(temp_dir),
                )


class EvaluationSummaryComparisonTests(unittest.TestCase):
    def test_pairs_outcomes_by_task_id_and_reports_gains_and_losses(self) -> None:
        baseline = {
            "model": "gemma-4-31b",
            "task_ids": ["a", "b", "c"],
            "results": [
                {"id": "a", "resolved": False},
                {"id": "b", "resolved": True},
                {"id": "c", "resolved": False},
            ],
            "resolved": 1,
            "total": 3,
        }
        candidate = {
            **baseline,
            "task_ids": ["c", "a", "b"],
            "results": [
                {"id": "c", "resolved": True},
                {"id": "a", "resolved": True},
                {"id": "b", "resolved": False},
            ],
            "resolved": 2,
        }

        report = compare_summaries(baseline, candidate)

        self.assertEqual(report["candidate_delta"], 1)
        self.assertEqual(report["gains"], ["a", "c"])
        self.assertEqual(report["losses"], ["b"])
        self.assertFalse(report["task_order_matches"])

    def test_rejects_different_models_or_task_sets(self) -> None:
        summary = {
            "model": "gemma-4-31b",
            "task_ids": ["a"],
            "results": [{"id": "a", "resolved": True}],
            "resolved": 1,
            "total": 1,
        }

        with self.assertRaisesRegex(ValueError, "model mismatch"):
            compare_summaries(summary, {**summary, "model": "gemma-4-12b"})
        with self.assertRaisesRegex(ValueError, "task-set mismatch"):
            compare_summaries(summary, {**summary, "task_ids": ["b"], "results": [{"id": "b", "resolved": True}]})

    def test_rejects_non_string_result_ids(self) -> None:
        summary = {
            "model": "gemma-4-31b",
            "task_ids": ["a"],
            "results": [{"id": {"unexpected": "object"}, "resolved": True}],
            "resolved": 1,
            "total": 1,
        }
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "summary.json"
            path.write_text(json.dumps(summary), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "result IDs must be strings"):
                read_summary(path)


if __name__ == "__main__":
    unittest.main()
