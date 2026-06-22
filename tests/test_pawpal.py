from pawpal_system import Task, Pet


def test_task_completion():
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        pet_name="Mochi",
        time="09:00"
    )

    assert task.completed == False

    task.mark_complete()

    assert task.completed == True


def test_task_addition_to_pet():
    pet = Pet("Mochi", "dog")

    task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="medium",
        pet_name="Mochi",
        time="08:00"
    )

    assert len(pet.get_tasks()) == 0

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].title == "Breakfast"