from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        pet_name="Mochi",
        time="09:00"
    )

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


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


def test_sort_tasks_by_time_returns_chronological_order():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    # Added out of order on purpose
    pet.add_task(Task("Evening walk", 20, "medium", "Mochi", "18:00"))
    pet.add_task(Task("Breakfast", 10, "high", "Mochi", "08:00"))
    pet.add_task(Task("Lunch", 15, "medium", "Mochi", "12:00"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time()

    sorted_times = [task.time for task in sorted_tasks]

    assert sorted_times == ["08:00", "12:00", "18:00"]


def test_sort_tasks_by_time_normalizes_single_digit_hour():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Lunch", 15, "medium", "Mochi", "12:00"))
    pet.add_task(Task("Breakfast", 10, "high", "Mochi", "9:00"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time()

    sorted_times = [task.time for task in sorted_tasks]

    assert sorted_times == ["09:00", "12:00"]


def test_filter_tasks_by_pet():
    owner = Owner("Brian")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    dog.add_task(Task("Morning walk", 30, "high", "Mochi", "09:00"))
    cat.add_task(Task("Give medication", 15, "high", "Luna", "12:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    mochi_tasks = scheduler.filter_tasks_by_pet("Mochi")

    assert len(mochi_tasks) == 1
    assert mochi_tasks[0].title == "Morning walk"
    assert mochi_tasks[0].pet_name == "Mochi"


def test_filter_tasks_by_status():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    completed_task = Task("Breakfast", 10, "high", "Mochi", "08:00")
    pending_task = Task("Evening walk", 20, "medium", "Mochi", "18:00")

    completed_task.mark_complete()

    pet.add_task(completed_task)
    pet.add_task(pending_task)

    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    completed_tasks = scheduler.filter_tasks_by_status(True)
    pending_tasks = scheduler.filter_tasks_by_status(False)

    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Breakfast"

    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Evening walk"


def test_daily_recurring_task_creates_next_day_task_when_completed():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00",
        frequency="daily"
    )

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    completed_task, next_task = scheduler.mark_task_complete("Mochi", "Breakfast")

    expected_next_date = (date.today() + timedelta(days=1)).isoformat()

    assert completed_task.completed is True
    assert next_task is not None
    assert next_task.title == "Breakfast"
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == expected_next_date

    assert len(pet.get_tasks()) == 2


def test_weekly_recurring_task_creates_next_week_task_when_completed():
    owner = Owner("Brian")
    pet = Pet("Luna", "cat")

    task = Task(
        title="Grooming",
        duration_minutes=30,
        priority="medium",
        pet_name="Luna",
        time="14:00",
        frequency="weekly"
    )

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    completed_task, next_task = scheduler.mark_task_complete("Luna", "Grooming")

    expected_next_date = (date.today() + timedelta(weeks=1)).isoformat()

    assert completed_task.completed is True
    assert next_task is not None
    assert next_task.title == "Grooming"
    assert next_task.completed is False
    assert next_task.frequency == "weekly"
    assert next_task.due_date == expected_next_date

    assert len(pet.get_tasks()) == 2


def test_once_task_does_not_create_next_task_when_completed():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    task = Task(
        title="Vet visit",
        duration_minutes=60,
        priority="high",
        pet_name="Mochi",
        time="10:00",
        frequency="once"
    )

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    completed_task, next_task = scheduler.mark_task_complete("Mochi", "Vet visit")

    assert completed_task.completed is True
    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner("Brian")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    dog.add_task(Task("Breakfast", 10, "high", "Mochi", "08:00"))
    cat.add_task(Task("Medication", 15, "high", "Luna", "08:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1

    task1, task2 = conflicts[0]

    assert task1.time == "08:00"
    assert task2.time == "08:00"


def test_detect_conflicts_returns_empty_list_when_no_conflicts():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Breakfast", 10, "high", "Mochi", "08:00"))
    pet.add_task(Task("Evening walk", 20, "medium", "Mochi", "18:00"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_pet_with_no_tasks_returns_empty_task_list():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_tasks_by_time() == []
    assert scheduler.filter_tasks_by_pet("Mochi") == []
    assert scheduler.filter_tasks_by_status(False) == []


def test_add_task_rejects_invalid_duration():
    pet = Pet("Mochi", "dog")

    task = Task(
        title="Invalid task",
        duration_minutes=0,
        priority="low",
        pet_name="Mochi",
        time="09:00"
    )

    with pytest.raises(ValueError):
        pet.add_task(task)


def test_task_gets_today_due_date_by_default():
    task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00"
    )

    assert task.due_date == date.today().isoformat()


def test_generate_daily_plan_only_uses_todays_pending_tasks():
    owner = Owner("Brian", available_minutes=60)
    pet = Pet("Mochi", "dog")

    tomorrow_date = (date.today() + timedelta(days=1)).isoformat()

    today_task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00"
    )

    tomorrow_task = Task(
        title="Tomorrow walk",
        duration_minutes=20,
        priority="medium",
        pet_name="Mochi",
        time="09:00",
        due_date=tomorrow_date
    )

    pet.add_task(today_task)
    pet.add_task(tomorrow_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    assert len(daily_plan) == 1
    assert daily_plan[0].title == "Breakfast"
    assert daily_plan[0].due_date == date.today().isoformat()


def test_generate_daily_plan_skips_completed_tasks():
    owner = Owner("Brian", available_minutes=60)
    pet = Pet("Mochi", "dog")

    completed_task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00"
    )

    pending_task = Task(
        title="Evening walk",
        duration_minutes=20,
        priority="medium",
        pet_name="Mochi",
        time="18:00"
    )

    completed_task.mark_complete()

    pet.add_task(completed_task)
    pet.add_task(pending_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    assert len(daily_plan) == 1
    assert daily_plan[0].title == "Evening walk"


def test_generate_daily_plan_respects_available_minutes():
    owner = Owner("Brian", available_minutes=25)
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Medication", 10, "high", "Mochi", "08:00"))
    pet.add_task(Task("Long walk", 30, "medium", "Mochi", "09:00"))
    pet.add_task(Task("Play time", 15, "low", "Mochi", "18:00"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    task_titles = [task.title for task in daily_plan]

    assert task_titles == ["Medication", "Play time"]


def test_detect_conflicts_ignores_completed_tasks():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    completed_task = Task("Breakfast", 10, "high", "Mochi", "08:00")
    pending_task = Task("Morning walk", 20, "medium", "Mochi", "08:00")

    completed_task.mark_complete()

    pet.add_task(completed_task)
    pet.add_task(pending_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_detect_conflicts_uses_due_date_and_time():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    tomorrow_date = (date.today() + timedelta(days=1)).isoformat()

    today_task = Task(
        title="Breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00"
    )

    tomorrow_task = Task(
        title="Tomorrow breakfast",
        duration_minutes=10,
        priority="high",
        pet_name="Mochi",
        time="08:00",
        due_date=tomorrow_date
    )

    pet.add_task(today_task)
    pet.add_task(tomorrow_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_mark_task_complete_returns_none_for_missing_task():
    owner = Owner("Brian")
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Breakfast", 10, "high", "Mochi", "08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    completed_task, next_task = scheduler.mark_task_complete("Mochi", "Missing task")

    assert completed_task is None
    assert next_task is None


def test_owner_rejects_duplicate_pet_names():
    owner = Owner("Brian")

    owner.add_pet(Pet("Mochi", "dog"))

    with pytest.raises(ValueError):
        owner.add_pet(Pet("Mochi", "cat"))