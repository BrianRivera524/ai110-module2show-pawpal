# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design for PawPal+ included four main classes: 'Owner', 'Pet', 
'Task', and 'Scheduler'. The 'Owner' class was responsible for storing the 
pet owner's basic information and managing a list of pets. The 'Pet' class 
represented each pet and stored details such as the pet's name, type, age, 
and its list of care tasks. The 'Task' class represented a single pet care 
activity, including information like the task name, duration, priority, 
time, frequency, and completion status. The 'Scheduler' class acted as the 
main logic layer for organizing tasks, generating a daily plan, sorting 
tasks by priority or time, and helping detect scheduling conflicts.

Overall, the design separated responsibilities so each class had a clear 
role. 'Owner' managed pets, 'Pet' managed its own tasks, 'Task' stored 
the details of individual care activities, and 'Scheduler' handled the 
planning logic.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design changed slightly during implementation. At first, I planned 
for most scheduling behavior to be handled directly inside the 'Pet' 
class, since each pet has its own tasks. However, I moved the scheduling 
logic into the 'Scheduler' class because it made the system easier to 
organize and extend. This change helped keep the 'Pet' class focused 
only on storing pet information and tasks, while the 'Scheduler' handled 
more advanced logic like sorting tasks, filtering by priority, checking 
available time, and detecting possible conflicts.

I also realized that tasks needed more detailed attributes than I 
originally planned. For example, adding fields like duration, priority, 
time, and frequency made it easier to generate a realistic daily plan 
and support smarter scheduling behavior.


**Bulding Blocks**

For PawPal+, I identified four main objects for the system: 

Owner, Pet, Task, and Scheduler.

- The Owner class represents the pet owner using the app.

Attributes:

name: the owner's name
pets: a list of pets owned by the user
available_minutes: the amount of time the owner has available for pet care tasks

Methods:

add_pet(pet): adds a pet to the owner's list
get_pets(): returns the owner's pets
get_all_tasks(): returns all tasks across all pets

- The Pet class represents an individual pet.

Attributes:

name: the pet's name
species: the type of pet, such as dog, cat, or other
tasks: a list of care tasks assigned to the pet

Methods:

add_task(task): adds a care task to the pet
remove_task(task_title): removes a task by title
get_tasks(): returns the pet's tasks

- The Task class represents one pet care activity.

Attributes:

title: the name of the task, such as feeding, walking, or medication
duration_minutes: how long the task takes
priority: the importance of the task, such as low, medium, or high
time: the preferred or scheduled time for the task
frequency: how often the task repeats, such as once, daily, or weekly
completed: whether the task has been completed

Methods:

mark_complete(): marks the task as completed
mark_incomplete(): marks the task as not completed
is_recurring(): checks whether the task repeats
summary(): returns a readable description of the task

- The Scheduler class is the main planning logic for the app.

Attributes:

owner: the owner whose pets and tasks are being scheduled

Methods:

get_all_tasks(): gathers all tasks from all pets
sort_tasks_by_time(): sorts tasks by scheduled time
sort_tasks_by_priority(): sorts tasks by priority
filter_tasks_by_pet(pet_name): filters tasks for one pet
filter_tasks_by_status(completed): filters tasks by completion status
generate_daily_plan(available_minutes): creates a daily plan based on time and priority
detect_conflicts(): checks for tasks scheduled at the same time

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considers a few main constraints: task time, 
task priority, task duration, completion status, frequency, 
and the owner's available care time. Time is used to sort 
tasks into a readable schedule, priority is used to decide 
which tasks should be handled first, duration is used to 
make sure the daily plan fits within the owner's available 
minutes, and completion status is used so completed tasks 
are not included again in the daily plan.

I decided that priority and available time mattered the 
most because the main goal of PawPal+ is to help a pet 
owner choose what care tasks can realistically be completed 
in a day. High-priority tasks, such as medication or feeding, 
should be scheduled before lower-priority tasks, such as play 
time. I also kept the time format simple by using 24-hour 
HH:MM strings, which makes sorting tasks easier while keeping 
the code readable.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that conflict detection 
only checks for exact time matches. For example, it can detect 
two tasks both scheduled at '09:00', but it does not detect 
overlapping durations, such as a 30-minute task at '09:00' 
and another task at '09:15'. I chose this simpler approach 
because it keeps the scheduler easier to understand while 
still demonstrating basic conflict detection. In a future 
version, I could improve this by converting task times into 
real time objects and comparing start and end times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
