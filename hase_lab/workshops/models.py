from dataclasses import dataclass, field


@dataclass
class Student:
    student_id: str
    free_slots: set[str]
    interests: set[str]
    registrations: list[str] = field(default_factory=list)


@dataclass
class Workshop:
    item_id: str
    title: str
    topic: str
    slot: str
    capacity: int
    attendees: list[str] = field(default_factory=list)
