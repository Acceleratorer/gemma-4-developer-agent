from __future__ import annotations

import json
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
