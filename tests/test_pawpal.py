from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_sort_by_time_orders_tasks_by_preferred_start_then_priority_and_duration() -> None:
    task_one = Task(title="Feed pet", duration_minutes=20, priority="low", preferred_start_minutes=600)
    task_two = Task(title="Walk pet", duration_minutes=15, priority="high", preferred_start_minutes=540)
    task_three = Task(title="Medication", duration_minutes=10, priority="high", preferred_start_minutes=540)
    task_four = Task(title="Nap time", duration_minutes=25, priority="medium")

    scheduler = Scheduler(owner=Owner(name="Avery"))
    scheduler.task_pool = [task_one, task_two, task_three, task_four]

    scheduler.sort_by_time()

    assert scheduler.task_pool[0] is task_three
    assert scheduler.task_pool[1] is task_two
    assert scheduler.task_pool[2] is task_one
    assert scheduler.task_pool[3] is task_four


def test_filter_tasks_by_completion_keeps_only_pending_tasks() -> None:
    pending_task = Task(title="Pending task", duration_minutes=10, priority="medium")
    completed_task = Task(title="Completed task", duration_minutes=15, priority="high", completed=True)

    scheduler = Scheduler(owner=Owner(name="Avery"))
    scheduler.task_pool = [pending_task, completed_task]

    scheduler.filter_tasks_by_completion(completed=False)

    assert scheduler.task_pool == [pending_task]


def test_filter_tasks_by_pet_name_is_case_insensitive() -> None:
    owner = Owner(name="Avery")
    luna = Pet(name="Luna", species="Cat")
    milo = Pet(name="Milo", species="Dog")
    owner.add_pet(luna)
    owner.add_pet(milo)

    luna_task = Task(title="Feed Luna", duration_minutes=10, priority="medium")
    milo_task = Task(title="Walk Milo", duration_minutes=20, priority="low")

    luna.add_task(luna_task)
    milo.add_task(milo_task)

    scheduler = Scheduler(owner=owner)
    scheduler.task_pool = owner.get_all_tasks()

    scheduler.filter_tasks_by_pet_name("lUNA")

    assert scheduler.task_pool == [luna_task]


def test_mark_complete_creates_next_recurring_task() -> None:
    task = Task(
        title="Daily meds",
        description="Give daily medication",
        duration_minutes=10,
        priority="high",
        required=True,
        recurrence="daily",
        scheduled_date=date(2026, 7, 1),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.title == task.title
    assert next_task.recurrence == task.recurrence
    assert next_task.scheduled_date == date(2026, 7, 2)
    assert next_task.pet_name == task.pet_name


def test_detect_conflicts_finds_shared_start_and_overlap_warnings() -> None:
    owner = Owner(name="Avery")
    pet = Pet(name="Milo", species="Dog")
    owner.add_pet(pet)

    first_task = Task(title="Morning walk", duration_minutes=45, priority="high", preferred_start_minutes=540)
    second_task = Task(title="Breakfast refill", duration_minutes=15, priority="low", preferred_start_minutes=540)
    third_task = Task(title="Vet reminder", duration_minutes=20, priority="medium", preferred_start_minutes=550)

    pet.add_task(first_task)
    pet.add_task(second_task)
    pet.add_task(third_task)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()

    assert any("share the same preferred start time" in warning for warning in conflicts)
    assert any("overlaps" in warning for warning in conflicts)


def test_generate_daily_plan_schedules_tasks_within_available_time() -> None:
    owner = Owner(name="Avery", available_minutes_per_day=90)
    pet = Pet(name="Milo", species="Dog")
    owner.add_pet(pet)

    morning_walk = Task(title="Morning walk", duration_minutes=30, priority="high", preferred_start_minutes=540)
    feed_pet = Task(title="Feed pet", duration_minutes=20, priority="medium", preferred_start_minutes=600)
    play_time = Task(title="Play time", duration_minutes=40, priority="low", preferred_start_minutes=660)

    pet.add_task(morning_walk)
    pet.add_task(feed_pet)
    pet.add_task(play_time)

    scheduler = Scheduler(owner=owner, day_start=8, day_end=18)
    scheduler.task_pool = owner.get_all_tasks()

    plan = scheduler.generate_daily_plan()

    assert len(plan.scheduled_tasks) == 3
    assert [scheduled.task.title for scheduled in plan.scheduled_tasks] == [
        "Morning walk",
        "Feed pet",
        "Play time",
    ]
    assert plan.scheduled_tasks[0].start_time == "08:00"
    assert plan.scheduled_tasks[-1].end_time == "09:30"
