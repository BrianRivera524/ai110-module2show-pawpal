from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(tasks):
    """Print the schedule in a readable format."""
    print("Today's Schedule")
    print("----------------")

    if not tasks:
        print("No tasks scheduled for today.")
        return

    for task in tasks:
        print(f"{task.time} - {task.title}")
        print(f"   Pet: {task.pet_name}")
        print(f"   Duration: {task.duration_minutes} minutes")
        print(f"   Priority: {task.priority}")
        print()


def main():
    owner = Owner("Brian", available_minutes=90)

    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")

    dog.add_task(Task("Morning walk", 30, "high", "Mochi", "09:00"))
    dog.add_task(Task("Breakfast", 10, "medium", "Mochi", "08:00"))
    cat.add_task(Task("Give medication", 15, "high", "Luna", "12:00"))
    cat.add_task(Task("Play time", 20, "low", "Luna", "18:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    todays_schedule = scheduler.sort_tasks_by_time()

    print_schedule(todays_schedule)


if __name__ == "__main__":
    main()