"""Cache automatic checks by saved source content; record local observations."""
import hashlib
import json
import subprocess
import sys
import threading
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TASKS = ("workshops", "reviews", "buddies")


class LiveChecks:
    def __init__(self, root):
        self.root = Path(root)
        self.cache = {}
        self.locks = {task: threading.Lock() for task in TASKS}

    def sources(self, task):
        paths = list((self.root / "hase_lab" / task).glob("*.py"))
        paths += list((self.root / "tests").glob(f"test_{task}_step*.py"))
        paths += [self.root / "hase_lab" / "__init__.py", self.root / "hase_lab" / "checks.py",
                  self.root / "tests" / "__init__.py"]
        return {str(path.relative_to(self.root)): path.read_bytes() for path in sorted(paths) if path.exists()}

    @staticmethod
    def fingerprint(sources):
        digest = hashlib.sha256()
        for name, content in sorted(sources.items()):
            digest.update(name.encode())
            digest.update(b"\0")
            digest.update(content)
            digest.update(b"\0")
        return digest.hexdigest()

    def status(self, task, retry=False):
        if task not in TASKS:
            raise ValueError("Unknown task")
        with self.locks[task]:
            sources = self.sources(task)
            fingerprint = self.fingerprint(sources)
            previous = self.cache.get(task)
            if previous and previous["fingerprint"] == fingerprint and not retry:
                return previous
            try:
                process = subprocess.run([sys.executable, "-B", "-m", "hase_lab.checks", task],
                    cwd=self.root, capture_output=True, text=True, timeout=8)
                if process.returncode:
                    report = {"steps": [], "all_passed": False,
                              "error": process.stderr[-5000:] or "Checks could not run."}
                else:
                    report = json.loads(process.stdout)
            except subprocess.TimeoutExpired:
                report = {"steps": [], "all_passed": False,
                          "error": "Checks exceeded eight seconds. Check for a loop, save, then retry."}
            except (ValueError, OSError) as exc:
                report = {"steps": [], "all_passed": False, "error": str(exc)}
            # Never present old green results if code was saved during execution.
            if self.fingerprint(self.sources(task)) != fingerprint:
                return {"stale": True, "all_passed": False}
            report.update(task=task, fingerprint=fingerprint,
                          checked_at=datetime.now(timezone.utc).isoformat())
            self.cache[task] = report
            try:
                self.record(task, report, sources)
            except OSError as exc:
                report["log_warning"] = f"Local log could not be saved: {exc}"
            return report

    def record(self, task, report, sources):
        directory = self.root / "study_data" / "automatic" / task
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": "automatic_check", **report}) + "\n")
        if report["all_passed"]:
            for name in ("first-passing-source.zip", "latest-passing-source.zip"):
                target = directory / name
                if name.startswith("first") and target.exists():
                    continue
                with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
                    for path, content in sources.items():
                        archive.writestr(path, content)
