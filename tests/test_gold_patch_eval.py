from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evals.build_gold_patch_eval import build_notebook


class GoldPatchEvalBuilderTests(unittest.TestCase):
    def test_both_mode_builds_paired_gold_and_empty_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            notebook_path, metadata_path = build_notebook(
                "dev-valid-unseen",
                Path(temporary_dir),
                "accelra/test-patch-controls",
                "Test Patch Controls",
                patch_mode="both",
            )

            notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            code = "".join(notebook["cells"][1]["source"])
            compile(code, str(notebook_path), "exec")

        self.assertIn("PATCH_MODES = ['gold', 'empty']", code)
        self.assertIn('agent_patch = task.patch if patch_mode == "gold" else ""', code)
        self.assertEqual(metadata["enable_gpu"], False)
        self.assertEqual(metadata["enable_tpu"], False)


if __name__ == "__main__":
    unittest.main()
