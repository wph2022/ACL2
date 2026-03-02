from __future__ import annotations

import json
import subprocess
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Iterable


class AdbService:
    def run(self, args: Iterable[str], timeout: int = 30) -> str:
        cmd = ["adb", *args]
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return completed.stdout if completed.returncode == 0 else completed.stderr


class LogIO:
    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        return Path(path).read_text(encoding=encoding, errors="ignore")

    def read_folder(self, folder: str) -> dict[str, str]:
        data: dict[str, str] = {}
        for file in Path(folder).glob("*.log"):
            data[file.name] = self.read_file(str(file))
        return data


class RuleManager:
    def __init__(self, rule_path: str):
        self.rule_path = Path(rule_path)
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        if not self.rule_path.exists():
            return {}
        return json.loads(self.rule_path.read_text(encoding="utf-8"))


class TaskRunner:
    def __init__(self):
        self._pool = ThreadPoolExecutor(max_workers=2)
        self._futures: list[Future] = []

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        f = self._pool.submit(fn, *args, **kwargs)
        self._futures.append(f)
        return f

    def cancel_all(self) -> None:
        for f in self._futures:
            f.cancel()
        self._futures.clear()
