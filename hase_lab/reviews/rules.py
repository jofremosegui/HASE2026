from .models import Reviewer, Project


def eligible(student: Reviewer, items: dict[str, Project]) -> list[Project]:
    """Return eligible items without changing input data. See task step 1."""
    return [p for p in items.values()
            if p.team == student.team
            and len(p.reviewers) < p.capacity
            and p.item_id not in student.assignments]
