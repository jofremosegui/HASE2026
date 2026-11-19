from dataclasses import dataclass, field


@dataclass
class Learner:
    student_id: str
    languages: set[str]
    goals: set[str]
    memberships: list[str] = field(default_factory=list)


@dataclass
class StudyGroup:
    item_id: str
    title: str
    topic: str
    language: str
    capacity: int
    members: list[str] = field(default_factory=list)
