"""Local study commands. Standard library only; no automatic uploads."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "study_data"
TASKS = ("workshops", "reviews", "buddies")
TOP_FILES = ("README.md", "AGENTS.md", ".gitignore", "study.py", "serve.py")
SOURCE_DIRS = ("hase_lab", "tests", "tasks", "web")

def now():
    return datetime.now(timezone.utc).isoformat()

def load_session(task):
    path = DATA / task / "session.json"
    return json.loads(path.read_text()) if path.exists() else None

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

def event(task, kind, **values):
    directory = DATA / task
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"at": now(), "event": kind, **values}) + "\n")

def source_files():
    for name in TOP_FILES:
        path = ROOT / name
        if path.is_file() and not path.is_symlink():
            yield path
    for name in SOURCE_DIRS:
        for path in sorted((ROOT / name).rglob("*")):
            if (path.is_file() and not path.is_symlink()
                and not any(part.startswith(".") or part == "__pycache__"
                            for part in path.relative_to(ROOT).parts)
                and path.suffix not in (".pyc", ".pyo")):
                yield path

def fingerprint():
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in source_files()}

class LoggedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []
        self.started = {}

    def startTest(self, test):
        self.started[test.id()] = time.monotonic()
        super().startTest(test)

    def record(self, test, outcome):
        self.records.append({"test": test.id(), "outcome": outcome,
                             "seconds": round(time.monotonic() - self.started.get(test.id(), time.monotonic()), 6)})

    def addSuccess(self, test):
        self.record(test, "passed")
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.record(test, "failed")
        super().addFailure(test, err)

    def addError(self, test, err):
        self.record(test, "error")
        super().addError(test, err)

    def addSkip(self, test, reason):
        self.record(test, "skipped")
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.records.append({"test": test.id(), "subtest": str(subtest),
                                 "outcome": "failed" if issubclass(err[0], test.failureException) else "error"})
        super().addSubTest(test, subtest, err)

def run_tests(args):
    session = load_session(args.task)
    if session and session.get("finished_at"):
        raise SystemExit("This task has finished. Do not run further participant tests.")
    if session is None:
        print("Practice run: no active timed session. Start the task before study work.")
    pattern = f"test_{args.task}_step{args.step}.py" if args.step else f"test_{args.task}_step*.py"
    began = time.monotonic()
    event(args.task, "tests_started", step=args.step, practice=session is None)
    try:
        suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern=pattern,
                                                   top_level_dir=str(ROOT))
        result = unittest.TextTestRunner(verbosity=2, resultclass=LoggedResult).run(suite)
    except Exception as exc:
        event(args.task, "tests_error", error=str(exc), step=args.step)
        raise
    event(args.task, "tests_completed", step=args.step, count=result.testsRun,
          success=result.wasSuccessful() and result.testsRun > 0, records=result.records,
          duration_seconds=round(time.monotonic() - began, 6), source_hashes=fingerprint())
    return 0 if result.wasSuccessful() and result.testsRun else 1

def start(args):
    if load_session(args.task):
        raise SystemExit("This task already has a session. Ask the researcher; do not overwrite it.")
    for task in TASKS:
        other = load_session(task)
        if other and not other.get("finished_at"):
            raise SystemExit(f"Finish the active task ({task}) first.")
        if other and other["participant"] != args.participant:
            raise SystemExit("Participant ID differs from the existing session.")
    value = {"participant": args.participant, "task": args.task, "condition": args.condition,
             "started_at": now(), "limit_seconds": 600, "source_hashes": fingerprint()}
    write_json(DATA / args.task / "session.json", value)
    (DATA / "chats").mkdir(exist_ok=True)
    event(args.task, "task_started", participant=args.participant, condition=args.condition)
    print(f"Started {args.task}: 10 minutes. Read tasks/{args.task}.md. Stop when time is called.")

def finish(args):
    value = load_session(args.task)
    if not value:
        raise SystemExit("No session found. Start the task first.")
    if value.get("finished_at"):
        raise SystemExit("Already finished. The original snapshot is preserved.")
    ended = now()
    snapshot = DATA / args.task / "finished_source.zip"
    hashes = fingerprint()
    with zipfile.ZipFile(snapshot, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files():
            archive.write(path, str(path.relative_to(ROOT)))
    value.update(finished_at=ended,
                 elapsed_seconds=(datetime.fromisoformat(ended) - datetime.fromisoformat(value["started_at"])).total_seconds(),
                 finished_source_hashes=hashes)
    write_json(DATA / args.task / "session.json", value)
    event(args.task, "task_finished", elapsed_seconds=value["elapsed_seconds"], snapshot=snapshot.name)
    print(f"Saved snapshot after {value['elapsed_seconds']:.1f} seconds. Stop editing; save the chat and answer the questionnaire without AI.")

def submit(args):
    for task in TASKS:
        session = load_session(task)
        if not session or not session.get("finished_at"):
            raise SystemExit(f"Task {task} has not finished. Finish all tasks, even incomplete ones.")
        if session["participant"] != args.participant:
            raise SystemExit("Participant ID differs from the recorded sessions.")
    directory = ROOT / "submissions"
    directory.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = directory / f"{args.participant}_{stamp}.zip"
    with zipfile.ZipFile(target, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files():
            archive.write(path, str(path.relative_to(ROOT)))
        for path in sorted(DATA.rglob("*")):
            if path.is_file() and not path.is_symlink() and not any(p.startswith(".") for p in path.relative_to(DATA).parts):
                archive.write(path, str(path.relative_to(ROOT)))
    chats = list((DATA / "chats").glob("*"))
    print(f"Created {target}")
    print(f"Found {len(chats)} chat files. Check that all three complete conversations and required answers are included before sending.")
    print("Nothing has been uploaded.")

def participant(value):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", value):
        raise argparse.ArgumentTypeError("Use a short anonymous ID containing letters, digits, _ or -.")
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    p = sub.add_parser("start")
    p.add_argument("task", choices=TASKS)
    p.add_argument("--participant", type=participant, required=True)
    p.add_argument("--condition", choices=("minimal", "concise", "detailed"), required=True)
    p = sub.add_parser("tests")
    p.add_argument("task", choices=TASKS)
    p.add_argument("--step", type=int, choices=(1, 2, 3))
    p = sub.add_parser("finish")
    p.add_argument("task", choices=TASKS)
    p = sub.add_parser("submit")
    p.add_argument("--participant", type=participant, required=True)
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10+ is required.")
    if args.command == "check":
        for task in TASKS:
            subprocess.run([sys.executable, "-B", "-m", "hase_lab.preview", task], cwd=ROOT,
                           check=True, stdout=subprocess.DEVNULL)
        print(f"Python {sys.version.split()[0]}: all three modules and previews load. No external dependencies needed.")
        print("Acceptance tests intentionally fail in the starter repository.")
    elif args.command == "tests":
        return run_tests(args)
    else:
        {"start": start, "finish": finish, "submit": submit}[args.command](args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
