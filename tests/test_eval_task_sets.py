from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _task_ids(name: str) -> list[str]:
    path = ROOT / "evals" / name
    return json.loads(path.read_text(encoding="utf-8"))


class EvaluationTaskSetTests(unittest.TestCase):
    def test_scorable_selection_set_preserves_the_unseen_holdout(self) -> None:
        training = _task_ids("dev-valid-training-gold-verified-task-ids.json")
        selection = _task_ids("dev-valid-training-gold-scorable-54-task-ids.json")
        holdout = _task_ids("dev-valid-unseen-gold-verified-task-ids.json")

        self.assertEqual(len(training), 44)
        self.assertEqual(len(selection), 54)
        self.assertEqual(len(set(selection)), 54)
        self.assertTrue(set(training).issubset(selection))
        self.assertTrue(set(selection).isdisjoint(holdout))


if __name__ == "__main__":
    unittest.main()
