from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time: str = ""
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        pass

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        pass

    def is_recurring(self):
        """Return True if this task repeats daily or weekly."""
        pass

    def summary(self):
        """Return a readable summary of the task."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a care task to this pet."""
        pass

    def remove_task(self, task_title):
        """Remove a task from this pet by title."""
        pass

    def get_tasks(self):
        """Return this pet's tasks."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int = 60
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner."""
        pass

    def get_pets(self):
        """Return all pets owned by this owner."""
        pass

    def get_all_tasks(self):
        """Return all tasks across all pets."""
        pass


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_all_tasks(self):
        """Get all tasks from the owner."""
        pass

    def sort_tasks_by_time(self):
        """Sort all tasks by scheduled time."""
        pass

    def sort_tasks_by_priority(self):
        """Sort all tasks by priority."""
        pass

    def filter_tasks_by_pet(self, pet_name):
        """Return tasks for one specific pet."""
        pass

    def filter_tasks_by_status(self, completed):
        """Return tasks based on completion status."""
        pass

    def generate_daily_plan(self, available_minutes):
        """Generate a daily plan based on available time and priority."""
        pass

    def detect_conflicts(self):
        """Detect tasks scheduled at the same time."""
        pass