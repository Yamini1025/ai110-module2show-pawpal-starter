from pawpal_system import Pet, Task


def test_task_completion_marks_task_as_completed() -> None:
    task = Task(
        title="Feed pet",
        description="Feed the dog breakfast.",
        duration_minutes=15,
        priority="medium",
    )

    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(name="Buddy", species="Dog")
    task = Task(
        title="Grooming",
        description="Brush the dog’s coat.",
        duration_minutes=20,
        priority="low",
    )

    initial_count = len(pet.get_task_list())
    pet.add_task(task)

    assert len(pet.get_task_list()) == initial_count + 1
    assert pet.get_task_list()[0] is task
