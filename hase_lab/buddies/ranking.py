from .models import Learner, StudyGroup


def ranked(student: Learner, candidates: list[StudyGroup]) -> list[StudyGroup]:
    """Return a newly sorted list of the supplied candidates. See task step 2.

    The caller provides candidates: do not apply eligibility filtering here.
    """
    # This placeholder preserves input order. Implement the ranking policy.
    return list(candidates)
