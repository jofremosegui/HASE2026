from .models import Learner, StudyGroup
from .rules import eligible

MAX_COMMITMENTS = 2


def join(student: Learner, items: dict[str, StudyGroup], item_id: str) -> bool:
    """Validate and record one commitment on both records. See task step 3.

    Return True on success, False on rejection. Rejection must leave all state
    unchanged. Unknown IDs are rejected, not raised as exceptions.
    """
    # Validate first, then update both records together.
    return False
