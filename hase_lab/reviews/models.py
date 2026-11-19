from dataclasses import dataclass, field


@dataclass
class Reviewer:
    student_id: str
    team: str
    expertise: set[str]
    assignments: list[str] = field(default_factory=list)


@dataclass
class Project:
    item_id: str
    title: str
    topic: str
    team: str
    capacity: int
    reviewers: list[str] = field(default_factory=list)
