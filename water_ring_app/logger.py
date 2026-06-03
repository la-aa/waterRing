from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
import traceback


def log_dir() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
    else:
        base = Path(__file__).resolve().parents[1]
    path = base / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def log_path() -> Path:
    return log_dir() / "app.log"


def write_exception(exc: BaseException) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = [
        f"[{stamp}] Unhandled exception",
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        "",
    ]
    with log_path().open("a", encoding="utf-8") as fh:
        fh.write("\n".join(payload))
