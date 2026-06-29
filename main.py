from pawpal_system import Owner, Pet, Task, Scheduler


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
    )
    task2 = Task(
        title="Medication reminder",
        description="Give Luna her daily vitamins.",
        duration_minutes=10,
        priority="medium",
        category="health",
        required=True,
    )
    task3 = Task(
        title="Play session",
        description="Spend time with both pets using toys.",
        duration_minutes=30,
        priority="low",
        category="bonding",
    )

    pet_one.add_task(task1)
    pet_two.add_task(task2)
    pet_one.add_task(task3)

    scheduler = Scheduler(owner=owner, day_start=8, day_end=18)
    plan = scheduler.generate_daily_plan()

    print(scheduler.explain_plan(plan))


if __name__ == "__main__":
    main()
