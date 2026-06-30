from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict, Optional


class Owner:
    """Store owner details, preferences, availability, and pets."""

    def __init__(
        self,
        name: str,
        contact_info: Optional[str] = None,
        preferences: Optional[Dict[str, str]] = None,
        available_minutes_per_day: int = 0,
    ):
        """Create an owner with contact and availability details."""
        self.name = name
        self.contact_info = contact_info
        self.preferences = preferences or {}
        self.available_minutes_per_day = available_minutes_per_day
        self.pets: List[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner if it is not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from the owner if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List["Task"]:
        """Return a combined list of tasks from all owned pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_task_list())
        return tasks

    def get_constraints(self) -> Dict[str, object]:
        """Return scheduling constraints and owner preferences."""
        return {
            "contact_info": self.contact_info,
            "preferences": self.preferences,
            "available_minutes_per_day": self.available_minutes_per_day,
        }


@dataclass
class Pet:
    """Represent a pet and the tasks assigned to that pet."""

    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to the pet if it is not already assigned."""
        if task not in self.tasks:
            task.pet_name = self.name
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from the pet if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_task_list(self) -> List["Task"]:
        """Return a copy of the pet's current task list."""
        return list(self.tasks)


@dataclass
class Task:
    """Describe a pet care task, including timing and recurrence data."""

    title: str
    description: Optional[str] = None
    duration_minutes: int = 0
    priority: str = "low"
    category: Optional[str] = None
    required: bool = False
    completed: bool = False
    pet_name: Optional[str] = None
    preferred_start_minutes: Optional[int] = None
    recurrence: Optional[str] = None
    scheduled_date: Optional[date] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed.

        If the task has a recurrence rule, create the next occurrence.
        """
        self.completed = True
        days = self._recurrence_days()
        if not self.recurrence or days is None:
            return None

        next_date = self.scheduled_date or date.today()
        next_date = next_date + timedelta(days=days)

        next_task = Task(
            title=self.title,
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            required=self.required,
            recurrence=self.recurrence,
            scheduled_date=next_date,
        )
        next_task.pet_name = self.pet_name
        return next_task

    def _recurrence_days(self) -> Optional[int]:
        """Convert a recurrence label into a number of days."""
        if not self.recurrence:
            return None
        recurrence_map = {
            "daily": 1,
            "weekly": 7,
        }
        return recurrence_map.get(self.recurrence.lower())

    def get_priority_score(self) -> int:
        """Calculate a numeric score for this task's priority."""
        priority_map = {
            "high": 3,
            "medium": 2,
            "low": 1,
        }
        score = priority_map.get(self.priority.lower(), 1)
        if self.required:
            score += 1
        return score

    def to_summary(self) -> str:
        """Return a one-line summary describing the task."""
        status = "Done" if self.completed else "Pending"
        return f"{self.title} ({self.priority.capitalize()} priority, {self.duration_minutes}m) - {status}"


@dataclass
class ScheduledTask:
    """Wrap a task with its planned start and end times."""

    task: Task
    start_time: str
    end_time: str

    def summary(self) -> str:
        """Return a formatted summary of the scheduled task."""
        return f"{self.start_time} - {self.end_time}: {self.task.title}"


@dataclass
class DailyPlan:
    """Hold the list of scheduled tasks for one day."""

    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)

    def get_summary(self) -> str:
        """Return a text summary of the daily schedule."""
        if not self.scheduled_tasks:
            return "No tasks scheduled for today."
        return "\n".join(task.summary() for task in self.scheduled_tasks)


class Scheduler:
    """Build and manage a daily task schedule for an owner."""

    def __init__(
        self,
        owner: Owner,
        task_pool: Optional[List[Task]] = None,
        day_start: int = 8,
        day_end: int = 18,
    ):
        """Initialize the scheduler with owner data and daily time boundaries."""
        self.owner = owner
        self.task_pool = task_pool or []
        self.day_start = day_start
        self.day_end = day_end

    def _get_task_pool(self) -> List[Task]:
        """Return the task pool from the scheduler or the owner if none is provided."""
        if self.task_pool:
            return list(self.task_pool)
        return self.owner.get_all_tasks()

    def generate_daily_plan(self) -> "DailyPlan":
        """Generate a daily schedule by assigning tasks into available time slots."""
        available_start = self.day_start * 60
        available_end = self.day_end * 60
        remaining_minutes = self.owner.available_minutes_per_day or (available_end - available_start)
        current_time = available_start

        tasks = self._get_task_pool()
        self.task_pool = tasks
        self.filter_tasks_by_completion(completed=False)
        self.sort_tasks_by_priority()
        self.sort_by_time()
        self.filter_tasks_by_time()

        scheduled_tasks: List[ScheduledTask] = []
        for task in self.task_pool:
            if task.duration_minutes <= 0:
                continue
            if current_time + task.duration_minutes > available_end:
                continue
            if task.duration_minutes > remaining_minutes:
                continue

            start_time = self._format_time(current_time)
            end_time = self._format_time(current_time + task.duration_minutes)
            scheduled_tasks.append(ScheduledTask(task=task, start_time=start_time, end_time=end_time))

            current_time += task.duration_minutes
            remaining_minutes -= task.duration_minutes
            if current_time >= available_end or remaining_minutes <= 0:
                break

        return DailyPlan(scheduled_tasks=scheduled_tasks)

    def sort_tasks_by_priority(self) -> None:
        """Sort the current task pool in descending priority order."""
        self.task_pool.sort(key=lambda task: task.get_priority_score(), reverse=True)

    def sort_by_time(self) -> None:
        """Sort tasks by preferred start time, then by priority and duration."""
        self.task_pool.sort(
            key=lambda task: (
                task.preferred_start_minutes
                if task.preferred_start_minutes is not None
                else float("inf"),
                -task.get_priority_score(),
                task.duration_minutes,
            )
        )

    def filter_tasks_by_completion(self, completed: bool = False) -> None:
        """Keep only tasks matching the requested completion status."""
        self.task_pool = [
            task
            for task in self.task_pool
            if task.completed == completed
        ]

    def filter_tasks_by_pet_name(self, pet_name: str) -> None:
        """Keep only tasks that belong to a pet with the given name."""
        self.task_pool = [
            task
            for task in self.task_pool
            if task.pet_name and task.pet_name.lower() == pet_name.lower()
        ]

    def detect_conflicts(self) -> List[str]:
        """Return warnings for lightweight scheduling conflicts.

        Detects same-pet tasks that share the same preferred start time
        or whose preferred time windows overlap.
        """
        tasks = [
            task
            for task in self._get_task_pool()
            if task.pet_name and task.preferred_start_minutes is not None
        ]
        tasks.sort(key=lambda task: (task.pet_name.lower(), task.preferred_start_minutes))

        warnings: List[str] = []
        for index in range(len(tasks)):
            task = tasks[index]
            for next_task in tasks[index + 1 :]:
                if task.pet_name.lower() != next_task.pet_name.lower():
                    break
                if task.preferred_start_minutes == next_task.preferred_start_minutes:
                    warnings.append(
                        f"Conflict: '{task.title}' and '{next_task.title}' for {task.pet_name} share the same preferred start time ({task.preferred_start_minutes})."
                    )
                task_end = task.preferred_start_minutes + task.duration_minutes
                if task_end > next_task.preferred_start_minutes:
                    warnings.append(
                        f"Conflict: '{task.title}' overlaps '{next_task.title}' for {task.pet_name}."
                    )
        return warnings

    def filter_tasks_by_time(self) -> None:
        """Remove tasks that cannot fit within the scheduler's daily window."""
        max_minutes = (self.day_end - self.day_start) * 60
        self.task_pool = [
            task
            for task in self.task_pool
            if 0 < task.duration_minutes <= max_minutes
        ]

    def explain_plan(self, plan: "DailyPlan") -> str:
        """Return a readable explanation of the daily plan."""
        if not plan.scheduled_tasks:
            return "The scheduler could not fit any tasks into today’s available time."
        lines = ["Daily plan:"]
        for scheduled in plan.scheduled_tasks:
            lines.append(f"- {scheduled.summary()}")
        return "\n".join(lines)

    @staticmethod
    def _format_time(minutes: int) -> str:
        """Format integer minutes into HH:MM text."""
        hour = minutes // 60
        minute = minutes % 60
        return f"{hour:02d}:{minute:02d}"
