from dataclasses import dataclass, field
from typing import List, Dict, Optional


class Owner:
    def __init__(
        self,
        name: str,
        contact_info: Optional[str] = None,
        preferences: Optional[Dict[str, str]] = None,
        available_minutes_per_day: int = 0,
    ):
        self.name = name
        self.contact_info = contact_info
        self.preferences = preferences or {}
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: List[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        pass

    def remove_pet(self, pet: "Pet") -> None:
        pass

    def get_constraints(self) -> Dict[str, object]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        pass

    def remove_task(self, task: "Task") -> None:
        pass

    def get_task_list(self) -> List["Task"]:
        pass


@dataclass
class Task:
    title: str
    description: Optional[str] = None
    duration_minutes: int = 0
    priority: str = "low"
    category: Optional[str] = None
    required: bool = False

    def get_priority_score(self) -> int:
        pass

    def to_summary(self) -> str:
        pass


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        task_pool: Optional[List[Task]] = None,
        day_start: int = 8,
        day_end: int = 18,
    ):
        self.owner = owner
        self.task_pool = task_pool or []
        self.day_start = day_start
        self.day_end = day_end

    def generate_daily_plan(self) -> "DailyPlan":
        pass

    def sort_tasks_by_priority(self) -> None:
        pass

    def filter_tasks_by_time(self) -> None:
        pass

    def explain_plan(self, plan: "DailyPlan") -> str:
        pass


class DailyPlan:
    pass
