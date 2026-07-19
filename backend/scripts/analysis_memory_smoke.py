"""Run the real analysis pipeline while measuring peak process memory."""

from __future__ import annotations

import argparse
import logging
import os
import threading
import time
from pathlib import Path

import psutil
from starlette.datastructures import UploadFile

from app.application.use_cases.analysis.analyze_track import analysis_service


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("track_a", type=Path)
    parser.add_argument("track_b", type=Path)
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.WARNING)
    process = psutil.Process(os.getpid())
    peak_rss = process.memory_info().rss
    stop = threading.Event()

    def monitor_memory() -> None:
        nonlocal peak_rss
        while not stop.wait(0.1):
            peak_rss = max(peak_rss, process.memory_info().rss)

    monitor = threading.Thread(target=monitor_memory, daemon=True)
    monitor.start()
    started = time.perf_counter()

    try:
        with args.track_a.open("rb") as file_a, args.track_b.open("rb") as file_b:
            result = analysis_service.analyze(
                UploadFile(filename=args.track_a.name, file=file_a),
                UploadFile(filename=args.track_b.name, file=file_b),
            )
    except Exception as exc:
        print(
            f"LOCAL_ANALYSIS_FAILED elapsed={time.perf_counter() - started:.2f}s "
            f"peak_rss={peak_rss / 1024 / 1024:.2f}MB "
            f"error={type(exc).__name__}: {exc}"
        )
        return 1
    finally:
        stop.set()
        monitor.join()

    print(
        f"LOCAL_ANALYSIS_OK elapsed={time.perf_counter() - started:.2f}s "
        f"peak_rss={peak_rss / 1024 / 1024:.2f}MB "
        f"analysis_id={result.analysis_id} "
        f"duration_a={result.track_a.duration:.2f}s "
        f"duration_b={result.track_b.duration:.2f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
