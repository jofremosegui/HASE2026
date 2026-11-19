from .models import Reviewer, Project


def ranked(student: Reviewer, candidates: list[Project]) -> list[Project]:
    """Return a newly sorted list of the supplied candidates. See task step 2.

    The caller provides candidates: do not apply eligibility filtering here.
    """
    # This placeholder preserves input order. Implement the ranking policy.
    return list(candidates)
