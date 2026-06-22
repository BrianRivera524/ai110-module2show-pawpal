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

I used AI throughout the project for design brainstorming, code 
structure, debugging, and reflection writing. At the beginning, 
I used AI to help identify the main objects in the system and 
translate them into a UML design. This helped me decide that Owner, 
Pet, Task, and Scheduler should be separate classes with different 
responsibilities.

During implementation, I used AI to help turn my UML into Python dataclasses 
and method stubs. After that, I used AI to improve the logic layer by adding 
sorting, filtering, recurring tasks, conflict detection, and Streamlit 
integration. I also used AI to review my code and point out possible 
weak spots, such as time formatting, duplicate pet names, and simple 
conflict detection.

The most helpful prompts were specific questions about one part of the project 
at a time. For example, asking how the Scheduler should retrieve all tasks from 
the owner's pets was helpful because it clarified the relationship between 
Scheduler, Owner, Pet, and Task. Asking how to simplify or improve a method 
was also useful because it helped me compare readability with performance.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not fully accept an AI suggestion was when the AI 
suggested making the scheduling system more advanced by using direct object 
references for pets, stronger ownership rules, and more complex overlap-based 
conflict detection. While those suggestions were technically better for a 
larger system, I decided not to implement all of them because they would 
make the project more complicated than necessary.

Instead, I kept a simpler design where each task stores a pet_name, and the 
scheduler checks for exact time conflicts. I evaluated the AI suggestion by 
comparing it to the project requirements and asking whether the extra complexity 
would actually improve the final project for this assignment. Since the 
assignment focused on demonstrating OOP, sorting, filtering, recurring tasks, 
and basic conflict detection, I decided that the simpler version was easier 
to understand and still met the requirements.

I verified the code by running main.py, testing the Streamlit app manually, and 
creating automated tests with pytest. This helped me make sure the important 
features worked instead of just accepting the AI's code without checking it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the main behaviors of the PawPal+ logic layer. I tested that a task can 
be marked complete, that adding a task to a pet increases the pet's task count, 
and that tasks can be sorted correctly by time. I also tested filtering by pet 
and filtering by completion status.

I also tested the smarter scheduling features. For recurring tasks, I tested that 
completing a daily task creates a new task for the following day, and that 
completing a weekly task creates a new task for the following week. I tested 
that one-time tasks do not create a new task when completed. I also tested 
conflict detection by creating two tasks at the exact same time and checking 
that the scheduler identifies the conflict.

These tests were important because they verify the core behavior of the system 
without needing to manually click through the Streamlit app every time. They 
also help catch bugs if I change the code later. For example, if sorting, 
recurrence, or conflict detection breaks, the tests should make that clear.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that my scheduler works correctly for the current project 
requirements. The tests cover the main features, including task completion, task 
addition, sorting by time, filtering, recurring task creation, and exact-time 
conflict detection. I would rate my confidence around 4 out of 5 stars because 
the system works for the intended use cases, but there are still some limitations.

If I had more time, I would test more edge cases. For example, I would test 
invalid time formats, duplicate task names for the same pet, empty owner data, 
and more advanced scheduling conflicts where tasks overlap by duration instead 
of starting at the exact same time. I would also test how the scheduler behaves 
when the owner has very little available time and only some tasks can fit into 
the daily plan.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I am most satisfied with is connecting the backend logic to the Streamlit UI. 
At first, the app and the logic layer felt separate, but after using st.session_state 
and the Scheduler class, the app became more realistic. Users can add pets, add tasks, 
complete tasks, filter tasks, generate a schedule, and check conflicts from the interface. 
I am also satisfied with the way the classes are separated. The Owner, Pet, Task, and 
Scheduler classes each have a clear responsibility, which made the project easier to 
build and debug. The recurring task logic was also a useful improvement because it made 
the scheduler feel more like a real pet care planning tool.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the conflict detection system. Right now, the 
scheduler only detects tasks that start at the exact same time. A better version would 
calculate each task's start and end time based on its duration, then detect overlapping 
tasks. For example, it should detect that a task from 09:00 to 09:30 conflicts with another 
task starting at 09:15. I would also improve time handling by using real Python datetime 
or time objects instead of only storing time as strings. This would make sorting and conflict 
detection more reliable. Another improvement would be allowing multiple pets and tasks to 
be edited or removed directly in the Streamlit app instead of only resetting the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that good system design depends on separating responsibilities clearly. 
When each class has one main purpose, the project is easier to understand and extend. For example, 
keeping pet information inside Pet, task information inside Task, and scheduling decisions inside 
Scheduler made the code more organized. I also learned that while AI is useful for brainstorming and 
improving code, but I still need to make the final decisions. Some AI suggestions were helpful, while 
others were more complicated than what the project needed. This project helped me practice using AI 
as a coding assistant while still checking the code, testing it, and deciding what design choices 
made the most sense.