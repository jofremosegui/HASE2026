from .models import Student, Workshop


def demo_data() -> tuple[Student, dict[str, Workshop]]:
    """Return fresh fictional data on every call; no other task is imported."""
    student = Student("s1", {"Mon 10", "Tue 14"}, {"testing", "teams"})
    items = {
        "w1": Workshop("w1", "Testing clinic", "testing", "Mon 10", 3, ["s2"]),
        "w2": Workshop("w2", "Team retrospective", "teams", "Tue 14", 3, []),
        "w3": Workshop("w3", "Research methods", "research", "Mon 10", 3, []),
        "w4": Workshop("w4", "Code review lab", "review", "Wed 09", 3, []),
        "w5": Workshop("w5", "Debugging clinic", "testing", "Mon 10", 1, ["s3"]),
    }
    return student, items
