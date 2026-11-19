from .models import Learner, StudyGroup


def demo_data() -> tuple[Learner, dict[str, StudyGroup]]:
    """Return fresh fictional data on every call; no other task is imported."""
    student = Learner("s1", {"English"}, {"testing", "teams"})
    items = {
        "g1": StudyGroup("g1", "Testing study circle", "testing", "English", 3, ["s2"]),
        "g2": StudyGroup("g2", "Teamwork discussion", "teams", "English", 3, []),
        "g3": StudyGroup("g3", "Research reading group", "research", "English", 3, []),
        "g4": StudyGroup("g4", "German discussion group", "teams", "German", 3, []),
        "g5": StudyGroup("g5", "Debugging study circle", "testing", "English", 1, ["s3"]),
    }
    return student, items
