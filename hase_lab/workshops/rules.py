from .models import Student, Workshop


def eligible(student: Student, items: dict[str, Workshop]) -> list[Workshop]:
    """Return eligible items without changing input data. See task step 1."""
    return [w for w in items.values()
            if w.slot in student.free_slots
            and len(w.attendees) <= w.capacity
            and w.item_id not in student.registrations]
