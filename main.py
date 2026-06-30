from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(label: str, tasks: list[Task]) -> None:
    print(f"\n{label}")
    if not tasks:
        print("  (none)")
        return
    for task in tasks:
        time_text = (
            f"preferred_start_minutes={task.preferred_start_minutes}"
            if task.preferred_start_minutes is not None
            else "no preferred start"
        )
        date_text = (
            f"scheduled_date={task.scheduled_date.isoformat()}"
            if task.scheduled_date is not None
            else "no scheduled date"
        )
        recurrence_text = task.recurrence or "no recurrence"
        status = "complete" if task.completed else "pending"
        print(
            f"  - {task.title} | pet={task.pet_name} | {date_text} | {time_text} | recurrence={recurrence_text} | {task.priority} | {status}"
        )


def print_task(label: str, task: Task) -> None:
    print(f"\n{label}")
    print_tasks("", [task])


def main() -> None:
    owner = Owner(name="Avery", contact_info="avery@example.com", available_minutes_per_day=240)

    pet_one = Pet(name="Milo", species="Dog", breed="Beagle", age=4)
    pet_two = Pet(name="Luna", species="Cat", breed="Siamese", age=2)

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    task1 = Task(
        title="Morning walk",
        description="Walk Milo around the neighborhood.",
        duration_minutes=45,
        priority="high",
        category="exercise",
        required=True,
        preferred_start_minutes=540,
    )
    task2 = Task(
        title="Medication reminder",
        description="Give Luna her daily vitamins.",
        duration_minutes=10,
        priority="medium",
        category="health",
        required=True,
        preferred_start_minutes=510,
    )
    task3 = Task(
        title="Play session",
        description="Spend time with both pets using toys.",
        duration_minutes=30,
        priority="low",
        category="bonding",
        preferred_start_minutes=600,
    )
    task4 = Task(
        title="Evening cuddle",
        description="Spend a few quiet minutes with Milo.",
        duration_minutes=15,
        priority="medium",
        category="bonding",
        preferred_start_minutes=1020,
    )
    recurring_task = Task(
        title="Daily meds",
        description="Give Luna her recurring daily medication.",
        duration_minutes=10,
        priority="high",
        category="health",
        required=True,
        preferred_start_minutes=480,
        recurrence="daily",
        scheduled_date=date.today(),
    )

    pet_one.add_task(task1)
    pet_two.add_task(task2)
    pet_one.add_task(task3)
    pet_one.add_task(task4)
    pet_two.add_task(recurring_task)

    conflict_task_a = Task(
        title="Vet reminder",
        description="Milo has an overlapping reminder.",
        duration_minutes=20,
        priority="medium",
        category="health",
        required=False,
        preferred_start_minutes=540,
    )
    conflict_task_b = Task(
        title="Breakfast refill",
        description="Another Milo task at the same time.",
        duration_minutes=15,
        priority="low",
        category="feeding",
        required=False,
        preferred_start_minutes=540,
    )
    pet_one.add_task(conflict_task_a)
    pet_one.add_task(conflict_task_b)

    scheduler = Scheduler(owner=owner, day_start=8, day_end=18)
    scheduler.task_pool = owner.get_all_tasks()

    print_tasks("Initial task order (non-chronological input):", scheduler.task_pool)

    scheduler.sort_by_time()
    print_tasks("After sort_by_time():", scheduler.task_pool)

    next_task = recurring_task.mark_complete()
    print_task("Original recurring task after completion:", recurring_task)
    print_task("New recurring task created by mark_complete():", next_task)

    scheduler.task_pool = owner.get_all_tasks()
    scheduler.filter_tasks_by_completion(completed=False)
    print_tasks("After filter_tasks_by_completion(completed=False):", scheduler.task_pool)

    scheduler.task_pool = owner.get_all_tasks()
    scheduler.filter_tasks_by_pet_name("Luna")
    print_tasks("After filter_tasks_by_pet_name('Luna'): ", scheduler.task_pool)

    scheduler.task_pool = owner.get_all_tasks()
    conflicts = scheduler.detect_conflicts()
    print("\nConflict warnings:")
    if not conflicts:
        print("  (no conflicts detected)")
    for warning in conflicts:
        print(f"  - {warning}")


if __name__ == "__main__":
    main()
