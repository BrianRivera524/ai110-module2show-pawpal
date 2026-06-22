from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


def normalize_time(time_str):
    """Convert time strings into 24-hour HH:MM format."""
    if not time_str:
        return ""

    hour, minute = time_str.split(":")
    return f"{int(hour):02d}:{int(minute):02d}"


def get_today_string():
    """Return today's date as a YYYY-MM-DD string."""
    return date.today().isoformat()


def get_next_due_date(due_date, frequency):
    """Return the next due date for a recurring task."""
    current_date = datetime.strptime(due_date, "%Y-%m-%d").date()

    if frequency == "daily":
        next_date = current_date + timedelta(days=1)
    elif frequency == "weekly":
        next_date = current_date + timedelta(weeks=1)
    else:
        next_date = current_date

    return next_date.isoformat()


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    pet_name: str
    time: str = ""
    frequency: str = "once"
    completed: bool = False
    due_date: str = field(default_factory=get_today_string)

    def __post_init__(self):
        """Normalize the task time after the task is created."""
        self.time = normalize_time(self.time)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.completed = False

    def is_recurring(self):
        """Return True if this task repeats daily or weekly."""
        return self.frequency in ["daily", "weekly"]

    def create_next_occurrence(self):
        """Create the next copy of a recurring task."""
        if not self.is_recurring():
            return None

        next_due_date = get_next_due_date(self.due_date, self.frequency)

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            pet_name=self.pet_name,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=next_due_date
        )

    def summary(self):
        """Return a readable summary of the task."""
        return (
            f"{self.due_date} {self.time} — {self.title} for {self.pet_name} "
            f"({self.duration_minutes} min) [priority: {self.priority}]"
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a care task to this pet."""
        if task.duration_minutes <= 0:
            raise ValueError("Task duration must be positive.")

        if task.pet_name != self.name:
            task.pet_name = self.name

        self.tasks.append(task)

    def remove_task(self, task_title):
        """Remove a task from this pet by title."""
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_tasks(self):
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int = 60
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner."""
        for existing_pet in self.pets:
            if existing_pet.name == pet.name:
                raise ValueError("A pet with this name already exists.")

        self.pets.append(pet)

    def get_pets(self):
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self):
        """Return all tasks across all pets."""
        all_tasks = []

        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())

        return all_tasks


class Scheduler:
    def __init__(self, owner):
        """Create a scheduler for one owner."""
        self.owner = owner

    def get_all_tasks(self):
        """Get all tasks from the owner."""
        return self.owner.get_all_tasks()

    def sort_tasks_by_time(self):
        """Sort all tasks by scheduled time."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def sort_tasks_by_priority(self):
        """Sort all tasks by priority."""
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        return sorted(
            self.get_all_tasks(),
            key=lambda task: priority_order.get(task.priority, 4)
        )

    def filter_tasks_by_pet(self, pet_name):
        """Return tasks for one specific pet."""
        return [
            task for task in self.get_all_tasks()
            if task.pet_name == pet_name
        ]

    def filter_tasks_by_status(self, completed):
        """Return tasks based on completion status."""
        return [
            task for task in self.get_all_tasks()
            if task.completed == completed
        ]

    def generate_daily_plan(self, available_minutes=None):
        """Generate a daily plan based on available time and priority."""
        if available_minutes is None:
            available_minutes = self.owner.available_minutes

        sorted_tasks = self.sort_tasks_by_priority()
        daily_plan = []
        used_minutes = 0

        for task in sorted_tasks:
            if task.completed:
                continue

            if used_minutes + task.duration_minutes <= available_minutes:
                daily_plan.append(task)
                used_minutes += task.duration_minutes

        return daily_plan

    def detect_conflicts(self):
        """Detect tasks scheduled at the same time."""
        conflicts = []
        seen_times = {}

        for task in self.get_all_tasks():
            if task.time == "":
                continue

            if task.time in seen_times:
                conflicts.append((seen_times[task.time], task))
            else:
                seen_times[task.time] = task

        return conflicts

    def mark_task_complete(self, pet_name, task_title):
        """Complete a task and create its next occurrence if recurring."""
        for pet in self.owner.get_pets():
            if pet.name == pet_name:
                for task in pet.get_tasks():
                    if task.title == task_title and not task.completed:
                        task.mark_complete()

                        next_task = task.create_next_occurrence()

                        if next_task is not None:
                            pet.add_task(next_task)

                        return task, next_task

        return None, None