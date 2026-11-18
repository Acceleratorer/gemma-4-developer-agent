"""Runtime embedded into a private Kaggle notebook for fixed-set evaluation."""

from __future__ import annotations

import asyncio
import concurrent.futures
import glob
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath


def _configure_environment() -> None:
    settings = {
        "TRANSFORMERS_NO_TF": "1",
        "TRANSFORMERS_NO_FLAX": "1",
        "TRANSFORMERS_OFFLINE": "1",
        "VLLM_NO_USAGE_STATS": "1",
        "VLLM_WORKER_MULTIPROC_METHOD": "spawn",
        "VLLM_ENGINE_READY_TIMEOUT_S": "1200",
        "VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS": "1",
        "NCCL_DEBUG": "WARN",
        "LITELLM_LOCAL_MODEL_COST_MAP": "True",
        "LITELLM_TELEMETRY": "False",
        "LITELLM_LOG": "WARNING",
        "OPENAI_API_KEY": "EMPTY",
        "LOCAL_API_KEY": "EMPTY",
        "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
        "OTEL_SDK_DISABLED": "true",
        "OTEL_PYTHON_DISABLED": "true",
    }
    os.environ.update(settings)
    for name in ("LiteLLM", "litellm", "httpx", "httpcore", "openai", "urllib3", "opentelemetry"):
        logging.getLogger(name).setLevel(logging.WARNING)


def _install_wheelhouse(wheelhouse: Path) -> None:
    if not wheelhouse.is_dir():
        raise FileNotFoundError(f"Wheelhouse input not found: {wheelhouse}")
    for pattern in (
        "/usr/local/lib/python*/dist-packages/*cutlass*.pth",
        "/usr/local/lib/python*/site-packages/*cutlass*.pth",
    ):
        for pth in glob.glob(pattern):
            try:
                os.unlink(pth)
            except OSError:
                pass

    staged = Path("/tmp/gemma4-wheelhouse")
    staged.mkdir(parents=True, exist_ok=True)
    for wheel in wheelhouse.glob("*.whl"):
        if "cutlass" in wheel.name.lower():
            continue
        name = wheel.name.replace("cu128", "+cu128") if "cu128" in wheel.name and "+" not in wheel.name else wheel.name
        target = staged / name
        if not target.exists():
            try:
                os.symlink(wheel, target)
            except OSError:
                shutil.copyfile(wheel, target)
    wheels = sorted(str(path) for path in staged.glob("*.whl"))
    if not wheels:
        raise RuntimeError("No compatible wheels were found in the competition wheelhouse")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--no-deps", "--force-reinstall", *wheels],
        check=True,
    )


def _materialize_agent(agent_files: dict[str, str], destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name, content in sorted(agent_files.items()):
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe submission path: {name}")
        path = destination.joinpath(*relative.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if not (destination / "agent.yaml").is_file():
        raise ValueError("Agent files do not contain a root agent.yaml")


def _run_sync(coro_or_fn, *args, **kwargs):
    if callable(coro_or_fn) and not asyncio.iscoroutine(coro_or_fn):
        fn = lambda: coro_or_fn(*args, **kwargs)
    else:
        fn = lambda: coro_or_fn
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop is not None and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(fn())).result()
    return asyncio.run(fn())


def run_dev_eval(
    agent_files: dict[str, str],
    task_ids: list[str],
    model_name: str,
    max_tool_calls: int = 40,
    max_time_minutes: float = 8.0,
) -> dict:
    _configure_environment()
    data_dir = Path("/kaggle/input/competitions/gemma-4-developer-agent")
    wheelhouse = Path("/kaggle/input/datasets/metric/gemma-4-developer-agent-wheelhouse")
    working_dir = Path("/kaggle/working")
    working_dir.mkdir(parents=True, exist_ok=True)
    _install_wheelhouse(wheelhouse)

    import torch
    import yaml
    from adk_submission import VllmConfig, VllmServer, discover_adapters, validate_directory
    from adk_submission.discovery import discover_declared_models
    from google.adk.agents.context_cache_config import ContextCacheConfig
    from google.adk.apps._configs import EventsCompactionConfig
    from swegemma.config import (
        ALLOWED_ADAPTER_EXTENSIONS,
        EvalConfig,
        build_submission_limits,
    )
    from swegemma.evaluate import Evaluator
    from swegemma.models import load_tasks

    task_path = data_dir / "tasks.jsonl"
    if not task_path.is_file():
        raise FileNotFoundError(f"Competition task file not found: {task_path}")
    agent_dir = working_dir / "agent"
    _materialize_agent(agent_files, agent_dir)

    limits, generation_constraints = build_submission_limits()
    for path in agent_dir.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Submission symlink is not allowed: {path}")
    validate_directory(agent_dir, limits=limits)
    declared_models = discover_declared_models(agent_dir)
    if declared_models != {model_name}:
        raise ValueError(f"Expected model {model_name}; found {sorted(declared_models)}")

    allowed_models = {
        "gemma-4-31b-it-qat-w4a16-ct",
        "gemma-4-12b-it-qat-w4a16-ct",
        "gemma-4-e4b-it-qat-w4a16-ct",
        "gemma-4-e2b-it-qat-w4a16-ct",
    }
    if model_name not in allowed_models:
        raise ValueError(f"Unsupported competition model: {model_name}")
    model_path = Path(f"/kaggle/input/models/google/gemma-4/other/{model_name}/2")
    if not model_path.exists():
        raise FileNotFoundError(f"Model input not attached: {model_path}")

    adapters = discover_adapters(str(agent_dir), adapter_extensions=ALLOWED_ADAPTER_EXTENSIONS)
    adapter_map = getattr(adapters, "adapters", None) or {}
    ranks = [info.rank for info in adapter_map.values() if getattr(info, "rank", None)]
    gpu_count = torch.cuda.device_count()
    if gpu_count < 4:
        raise RuntimeError(f"Expected the competition's 4-GPU environment, found {gpu_count}")

    server = VllmServer(
        VllmConfig(
            model=str(model_path),
            port=8000,
            host="127.0.0.1",
            tool_call_parser="gemma4",
            reasoning_parser="gemma4",
            max_model_len=32768,
            dtype="bfloat16" if torch.cuda.is_bf16_supported() else "auto",
            gpu_memory_utilization=0.90,
            enable_auto_tool_choice=True,
            enable_lora=bool(adapter_map),
            max_loras=max(1, len(adapter_map)),
            max_lora_rank=max(ranks) if ranks else 128,
            scheduler_reserve_full_isl=False,
            tensor_parallel_size=4,
            startup_timeout=1200,
            extra_args=(
                ("--hf-overrides", '{"architectures": ["Gemma4ForCausalLM"], "model_type": "gemma4"}')
                if model_name == "gemma-4-12b-it-qat-w4a16-ct"
                else ()
            ),
        ),
        adapter_manifest=adapters,
    )
    server.start()
    try:
        models = server.create_model_registry(
            aliases=[model_name], model_prefix="openai/", api_key=os.environ["LOCAL_API_KEY"]
        )
        tasks = load_tasks(task_path)
        by_id = {task.instance_id: task for task in tasks}
        missing = [task_id for task_id in task_ids if task_id not in by_id]
        if missing:
            raise ValueError(f"Unknown task IDs: {missing}")

        run_id = hashlib.sha256(
            (model_name + "\n" + "\n".join(task_ids) + "\n" + str(max_tool_calls) + "\n" + str(max_time_minutes)).encode()
        ).hexdigest()[:12]
        results_dir = working_dir / "dev_results" / run_id
        results_dir.mkdir(parents=True, exist_ok=True)
        eval_config = EvalConfig(
            tasks_path=task_path,
            snapshots_dir=data_dir / "snapshots",
            results_dir=results_dir,
            submission_dir=agent_dir,
            models=models,
            sandbox="subprocess",
            timeout_seconds=180,
            verification_timeout_seconds=300,
            max_time_minutes=max_time_minutes,
            max_tool_calls=max_tool_calls,
            max_turns=80,
            limits=limits,
            generation_constraints=generation_constraints,
            adapter_manifest=adapters,
            context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=1800, cache_intervals=10),
            events_compaction_config=EventsCompactionConfig(
                compaction_interval=15,
                overlap_size=2,
                token_threshold=14336,
                event_retention_size=5,
            ),
            graph_dir=data_dir / "graphs",
            embeddings_dir=data_dir / "embeddings",
            wheels_dir=data_dir / "wheels",
            verbose=False,
        )
        evaluator = Evaluator(eval_config)
        rows = []
        for index, task_id in enumerate(task_ids, start=1):
            task = by_id[task_id]
            print(f"[{index}/{len(task_ids)}] {task.instance_id} ({task.repo})")
            result = _run_sync(
                evaluator.evaluate_task,
                task=task,
                task_index=index,
                total_tasks=len(task_ids),
            )
            patch = (result.agent_patch or "").strip()
            row = {
                "id": task.instance_id,
                "repo": task.repo,
                "resolved": bool(result.resolved),
                "test_exit_code": result.test_exit_code,
                "patch_chars": len(patch),
                "tool_calls": result.tool_calls,
                "duration_seconds": result.duration_seconds,
                "error": getattr(result, "error", None),
            }
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False))

        resolved = sum(row["resolved"] for row in rows)
        summary = {
            "run_id": run_id,
            "model": model_name,
            "task_ids": task_ids,
            "resolved": resolved,
            "total": len(rows),
            "score": resolved / len(rows) if rows else 0.0,
            "results": rows,
        }
        (results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        (results_dir / "task_results.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
        )
        output_path = working_dir / f"dev-eval-{run_id}.json"
        output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"DEV_SCORE={resolved}/{len(rows)} ({summary['score']:.4f})")
        print(f"RESULT_FILE={output_path}")
        return summary
    finally:
        server.stop()
