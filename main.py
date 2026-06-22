from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(title, tasks):
    """Print tasks in a readable terminal format."""
    print(title)
    print("-" * len(title))

    if not tasks:
        print("No tasks found.")
        print()
        return

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(f"{task.due_date} {task.time} - {task.title}")
        print(f"   Pet: {task.pet_name}")
        print(f"   Duration: {task.duration_minutes} minutes")
        print(f"   Priority: {task.priority}")
        print(f"   Frequency: {task.frequency}")
        print(f"   Status: {status}")
        print()


def print_conflicts(conflicts):
    """Print conflict warnings in the terminal."""
    print("Conflict Check")
    print("--------------")

    if not conflicts:
        print("No conflicts found.")
        print()
        return

    for task1, task2 in conflicts:
        print(
            f"Warning: {task1.title} for {task1.pet_name} conflicts with "
            f"{task2.title} for {task2.pet_name} on {task1.due_date} at {task1.time}."
        )

    print()


def main():
    owner = Owner("Brian", available_minutes=90)

    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    dog.add_task(Task("Evening walk", 25, "medium", "Mochi", "18:00", "daily"))
    cat.add_task(Task("Give medication", 15, "high", "Luna", "08:00", "daily"))
    dog.add_task(Task("Breakfast", 10, "high", "Mochi", "08:00", "daily"))
    cat.add_task(Task("Play time", 20, "low", "Luna", "16:00", "weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    print_tasks("Today's Schedule Sorted by Time", scheduler.sort_tasks_by_time())

    print_tasks("Mochi's Tasks", scheduler.filter_tasks_by_pet("Mochi"))

    print_tasks("Pending Tasks", scheduler.filter_tasks_by_status(False))

    print_conflicts(scheduler.detect_conflicts())

    completed_task, next_task = scheduler.mark_task_complete("Mochi", "Breakfast")

    if completed_task:
        print(f"Completed task: {completed_task.title} for {completed_task.pet_name}")

    if next_task:
        print(f"Created next recurring task: {next_task.summary()}")

    print()

    print_tasks("Updated Tasks After Completing Breakfast", scheduler.sort_tasks_by_time())


if __name__ == "__main__":
    main()