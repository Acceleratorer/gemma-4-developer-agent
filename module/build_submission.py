"""Build deterministic, competition-shaped submission ZIP archives."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "module" / "agents"
ALLOWED_MODELS = {
    "gemma-4-31b-it-qat-w4a16-ct",
    "gemma-4-12b-it-qat-w4a16-ct",
    "gemma-4-e4b-it-qat-w4a16-ct",
    "gemma-4-e2b-it-qat-w4a16-ct",
}
ALLOWED_EXTENSIONS = {
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".py",
    ".json",
    ".safetensors",
}
MAX_UNPACKED_BYTES = 3 * 1024**3
ROOT_CONFIGS = {"agent.yaml", "agent.yml", "root_agent.yaml", "root_agent.yml"}
MODEL_LINE = re.compile(r"(?m)^(\s*model:\s*)([^\s#]+)(\s*(?:#.*)?$)")


def _relative_member(source: Path, path: Path) -> str:
    if path.is_symlink():
        raise ValueError(f"Symlinks are not permitted: {path}")
    resolved = path.resolve()
    if not resolved.is_relative_to(source):
        raise ValueError(f"Path escapes the agent directory: {path}")
    member = path.relative_to(source).as_posix()
    pure = PurePosixPath(member)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise ValueError(f"Unsafe archive path: {member}")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported submission file extension: {member}")
    return member


def _model_names(payloads: dict[str, bytes]) -> set[str]:
    names: set[str] = set()
    for member, content in payloads.items():
        if PurePosixPath(member).suffix.lower() not in {".yaml", ".yml"}:
            continue
        text = content.decode("utf-8")
        names.update(name for _, name, _ in MODEL_LINE.findall(text))
    return names


def validate_payloads(payloads: dict[str, bytes], model: str | None = None) -> None:
    root_configs = [name for name in payloads if name in ROOT_CONFIGS]
    if len(root_configs) != 1:
        raise ValueError("Submission must contain exactly one root agent YAML file")
    if not payloads:
        raise ValueError("Submission archive cannot be empty")
    if sum(map(len, payloads.values())) > MAX_UNPACKED_BYTES:
        raise ValueError("Submission exceeds the 3 GiB unpacked-size limit")

    names = _model_names(payloads)
    if not names or not names.issubset(ALLOWED_MODELS):
        raise ValueError(f"Submission must declare supported Gemma 4 models; found {sorted(names)}")
    if len(names) != 1:
        raise ValueError(f"All agents must use one base model; found {sorted(names)}")
    if model is not None and names != {model}:
        raise ValueError(f"Model override was not applied to every agent: found {sorted(names)}")


def build_submission(
    agent_dir: Path,
    output_path: Path,
    model: str | None = None,
    overwrite: bool = False,
) -> tuple[Path, str, tuple[str, ...]]:
    source = agent_dir.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Agent directory not found: {agent_dir}")
    if model is not None and model not in ALLOWED_MODELS:
        raise ValueError(f"Unsupported model: {model}")

    destination = output_path.resolve()
    if destination.is_relative_to(source):
        raise ValueError("Output archive must be outside the agent directory")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Output already exists; pass --overwrite to replace it: {destination}")

    payloads: dict[str, bytes] = {}
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            if path.is_symlink():
                raise ValueError(f"Symlinks are not permitted: {path}")
            continue
        member = _relative_member(source, path)
        content = path.read_bytes()
        if model is not None and PurePosixPath(member).suffix.lower() in {".yaml", ".yml"}:
            content_text, replacements = MODEL_LINE.subn(
                lambda match: f"{match.group(1)}{model}{match.group(3)}", content.decode("utf-8")
            )
            if replacements:
                content = content_text.encode("utf-8")
        payloads[member] = content

    validate_payloads(payloads, model)
    if len(payloads) > 10_000:
        raise ValueError("Submission exceeds the 10,000-file limit")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent, delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
        with zipfile.ZipFile(temporary_path, "w") as archive:
            for member, content in sorted(payloads.items()):
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with zipfile.ZipFile(temporary_path) as archive:
            if archive.testzip() is not None:
                raise ValueError("Generated archive failed CRC validation")
            archived = {info.filename: archive.read(info.filename) for info in archive.infolist()}
            validate_payloads(archived, model)
            if archived != payloads:
                raise ValueError("Generated archive content differs from the source files")
        if destination.exists() and not overwrite:
            raise FileExistsError(f"Output appeared during build; refusing to replace it: {destination}")
        os.replace(temporary_path, destination)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return destination, digest, tuple(sorted(payloads))


def main() -> None:
    agent_names = sorted(
        path.name
        for path in AGENTS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith("reference-")
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=agent_names, default="current")
    parser.add_argument("--model", choices=sorted(ALLOWED_MODELS))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    source = AGENTS_DIR / args.agent
    source_payloads = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
    }
    model = args.model or next(iter(_model_names(source_payloads)))
    suffix = model.removeprefix("gemma-4-").replace("-it-qat-w4a16-ct", "")
    output = args.output or ROOT / "dist" / f"{args.agent}-{suffix}.zip"
    path, digest, members = build_submission(source, output, args.model, args.overwrite)
    print(f"Built {path}")
    print(f"SHA-256: {digest}")
    print(f"Files ({len(members)}): {', '.join(members)}")


if __name__ == "__main__":
    main()
