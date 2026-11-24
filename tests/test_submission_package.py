from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from module.build_submission import (
    ALLOWED_MODELS,
    build_submission,
    validate_payloads,
)

ROOT = Path(__file__).resolve().parents[1]
CURRENT_AGENT = ROOT / "module" / "agents" / "current"
EXPECTED_MEMBERS = {
    "agent.yaml",
    "configs/sampling.yaml",
    "eval_config.yaml",
    "LICENSE.txt",
    "NOTICE.txt",
    "prompts/system.md",
}


class SubmissionPackageTests(unittest.TestCase):
    def test_archive_is_valid_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first.zip"
            second = Path(temp_dir) / "second.zip"
            build_submission(CURRENT_AGENT, first)
            build_submission(CURRENT_AGENT, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(set(archive.namelist()), EXPECTED_MEMBERS)
                self.assertIn(b"model: gemma-4-31b-it-qat-w4a16-ct", archive.read("agent.yaml"))

    def test_supported_small_model_override_reaches_every_agent(self) -> None:
        model = "gemma-4-e4b-it-qat-w4a16-ct"
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "small.zip"
            build_submission(CURRENT_AGENT, output, model=model)
            with zipfile.ZipFile(output) as archive:
                self.assertIn(f"model: {model}".encode(), archive.read("agent.yaml"))

    def test_existing_output_requires_explicit_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "submission.zip"
            output.write_bytes(b"keep")
            with self.assertRaises(FileExistsError):
                build_submission(CURRENT_AGENT, output)
            self.assertEqual(output.read_bytes(), b"keep")

    def test_rejects_unsupported_model_and_mixed_model_agents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                build_submission(CURRENT_AGENT, Path(temp_dir) / "bad.zip", model="not-a-gemma-model")

        payloads = {
            "agent.yaml": b"model: gemma-4-31b-it-qat-w4a16-ct\n",
            "sub_agents/worker.yaml": b"model: gemma-4-e4b-it-qat-w4a16-ct\n",
        }
        with self.assertRaises(ValueError):
            validate_payloads(payloads)

    def test_allowed_model_set_contains_only_competition_variants(self) -> None:
        self.assertEqual(
            ALLOWED_MODELS,
            {
                "gemma-4-31b-it-qat-w4a16-ct",
                "gemma-4-12b-it-qat-w4a16-ct",
                "gemma-4-e4b-it-qat-w4a16-ct",
                "gemma-4-e2b-it-qat-w4a16-ct",
            },
        )


if __name__ == "__main__":
    unittest.main()
