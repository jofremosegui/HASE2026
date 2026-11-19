"""Fresh-process rendering adapter. Kept outside participant task code."""
import importlib
import json
import sys
from dataclasses import asdict

META = {
    "workshops": ("register", "registrations", "attendees", "interests"),
    "reviews": ("assign", "assignments", "reviewers", "expertise"),
    "buddies": ("join", "memberships", "members", "goals"),
}

def preview(task, actions):
    if task not in META:
        raise ValueError("Unknown task")
    action, current, member, preferences = META[task]
    base = f"hase_lab.{task}"
    student, items = importlib.import_module(base + ".seed").demo_data()
    eligible = importlib.import_module(base + ".rules").eligible
    ranked = importlib.import_module(base + ".ranking").ranked
    commit = getattr(importlib.import_module(base + ".service"), action)
    outcomes = []
    for target in actions:
        outcomes.append({"item_id": target, "accepted": commit(student, items, target)})
    candidates = eligible(student, items)
    ordered = ranked(student, candidates)
    return {
        "task": task, "records": [asdict(item) for item in items.values()],
        "eligible": [item.item_id for item in candidates],
        "ranked": [item.item_id for item in ordered], "actions": outcomes,
        "commitments": getattr(student, current), "member_field": member,
        "preferences": sorted(getattr(student, preferences)),
    }

if __name__ == "__main__":
    print(json.dumps(preview(sys.argv[1], sys.argv[2:])))
