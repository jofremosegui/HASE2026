from .models import Learner, StudyGroup


def eligible(student: Learner, items: dict[str, StudyGroup]) -> list[StudyGroup]:
    """Return eligible items without changing input data. See task step 1."""
    return [g for g in items.values()
            if g.language not in student.languages
            and len(g.members) < g.capacity
            and g.item_id not in student.memberships]
