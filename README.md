# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

'''
## Sample Output

After running:

python main.py

The terminal prints:

Today's Schedule
----------------
08:00 - Breakfast
   Pet: Mochi
   Duration: 10 minutes
   Priority: medium

09:00 - Morning walk
   Pet: Mochi
   Duration: 30 minutes
   Priority: high

12:00 - Give medication
   Pet: Luna
   Duration: 15 minutes
   Priority: high

18:00 - Play time
   Pet: Luna
   Duration: 20 minutes
   Priority: low

'''

## 🧪 Testing PawPal+

'''
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
'''

Sample test output:

'''
# Paste your pytest output here
======= test session starts ========
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\river\Downloads\CodePath_TF_Tasks\ai110-module2show-pawpal
plugins: anyio-4.13.0
collected 13 items                                              

tests\test_pawpal.py .............                        [100%]

======== 13 passed in 0.07s ========
'''
Confidence Level: 4/5 stars

I am fairly confident in the system because the automated tests cover 
the main scheduling features, including sorting, filtering, recurring 
tasks, and conflict detection. I did not give it 5 stars because the 
current conflict detection only checks for exact time matches and 
does not yet detect overlapping durations.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

PawPal+ includes several smarter scheduling features to make the app more useful for a pet owner.

| Feature  |  Method  |  Description  |
| -------- | -------- | ------------- |
| Sort tasks by time | 'Scheduler.sort_tasks_by_time()' | Sorts all tasks by their scheduled time using 24-hour 'HH:MM' format. This helps display the daily schedule in the correct order. |

| Sort tasks by priority | 'Scheduler.sort_tasks_by_priority()' | Sorts tasks so higher-priority care tasks, such as feeding or medication, are considered before lower-priority tasks. |

| Filter tasks by pet | 'Scheduler.filter_tasks_by_pet(pet_name)' | Returns only the tasks that belong to a selected pet. This helps the owner view one pet's care plan at a time. |

| Filter tasks by status | 'Scheduler.filter_tasks_by_status(completed)' | Returns either completed or pending tasks. This helps the owner track what still needs to be done. |

| Generate daily plan | 'Scheduler.generate_daily_plan()' | Builds a daily plan using priority, task duration, completion status, and the owner's available care time. |

| Conflict detection | 'Scheduler.detect_conflicts()' | Checks for tasks scheduled at the exact same time and returns conflicts as warnings instead of crashing the program. |

| Recurring tasks | 'Task.create_next_occurrence()' and 'Scheduler.mark_task_complete()' | When a daily or weekly task is completed, the scheduler creates a new copy of that task for the next due date. |

One current tradeoff is that conflict detection only checks for exact time matches. 
For example, it detects two tasks both scheduled at '09:00', but it does not detect 
overlapping durations such as a 30-minute task at '09:00' and another task at '09:15'. 
This keeps the first version simpler and easier to understand.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open the app by running streamlit run app.py in the terminal.

2. Enter the owner information, including the owner's name and the 
number of minutes available for pet care tasks that day.

3. Add one or more pets by entering the pet's name and species, 
then clicking Add pet.

4. Add care tasks for each pet by selecting the pet, entering 
the task title, duration, priority, time in 24-hour HH:MM format, 
and frequency.

5. Review the Current Tasks table to confirm that the tasks were 
saved and are displayed in sorted order.

6. Use Complete Task to mark a task as finished. If the task is 
daily or weekly, the app automatically creates the next recurring task.

7. Use Filter Tasks by Pet or Filter Tasks by Status to view a smaller set of tasks.

8. Click Generate schedule to create a daily plan based on task priority, 
task duration, completion status, and the owner's available time.

9. Click Check for conflicts to see whether two tasks are scheduled 
at the exact same time.

10. Use Reset app to clear the current owner, pets, and tasks and start over.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
