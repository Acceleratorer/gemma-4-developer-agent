from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evals.kaggle_runtime import append_task_result


class KaggleRuntimeCheckpointTests(unittest.TestCase):
    def test_appends_each_completed_task_as_a_json_line(self) -> None:
        first = {"id": "fastapi_1", "resolved": True}
        second = {"id": "rich_2", "resolved": False, "note": "café"}

        with TemporaryDirectory() as temp_dir:
            checkpoint = Path(temp_dir) / "task_results.jsonl"
            append_task_result(checkpoint, first)
            append_task_result(checkpoint, second)

            rows = [json.loads(line) for line in checkpoint.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(rows, [first, second])


if __name__ == "__main__":
    unittest.main()
