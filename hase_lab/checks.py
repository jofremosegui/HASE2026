"""Run public checks for one module in a fresh process; emit machine-readable results."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

TASKS = ("workshops", "reviews", "buddies")
ROOT = Path(__file__).resolve().parent.parent


def check(task):
    if task not in TASKS:
        raise ValueError("Unknown task")
    steps = []
    for step in (1, 2, 3):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            suite = unittest.TestLoader().discover(str(ROOT / "tests"),
                       pattern=f"test_{task}_step{step}.py", top_level_dir=str(ROOT))
            result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        passed = result.wasSuccessful() and result.testsRun == 4 and not result.skipped
        steps.append({"step": step, "passed": passed, "total": result.testsRun,
                      "failures": len(result.failures), "errors": len(result.errors),
                      "output": output.getvalue()[-10000:]})
    return {"steps": steps, "all_passed": all(step["passed"] for step in steps)}


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1])))
