from .models import Reviewer, Project


def demo_data() -> tuple[Reviewer, dict[str, Project]]:
    """Return fresh fictional data on every call; no other task is imported."""
    student = Reviewer("s1", "team-a", {"testing", "teams"})
    items = {
        "p1": Project("p1", "Review quality study", "testing", "team-b", 3, ["s2"]),
        "p2": Project("p2", "Team wellbeing study", "teams", "team-c", 3, []),
        "p3": Project("p3", "Developer onboarding", "onboarding", "team-d", 3, []),
        "p4": Project("p4", "Our HASE project", "testing", "team-a", 3, []),
        "p5": Project("p5", "AI explanation study", "testing", "team-e", 1, ["s3"]),
        "p6": Project("p6", "Pair programming study", "teams", "team-f", 2, []),
        "p7": Project("p7", "Test feedback dashboard", "testing", "team-g", 2, ["s3"]),
        "p8": Project("p8", "Open-source mentoring", "onboarding", "team-h", 3, []),
    }
    return student, items
