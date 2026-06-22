import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ---------------------------------------------------------
# Session State Setup
# ---------------------------------------------------------
# Streamlit reruns this file every time a button is clicked.
# st.session_state keeps the Owner object saved between reruns.

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=60)

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app now connects the Streamlit UI to the backend logic in `pawpal_system.py`.

Use this app as your interactive demo to add pets, add tasks, and generate a schedule.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks
- Represent the pet and the owner
- Build a plan/schedule for a day
- Explain the plan
"""
    )

st.divider()

# ---------------------------------------------------------
# Owner Setup
# ---------------------------------------------------------

st.subheader("Owner Information")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

available_minutes = st.number_input(
    "Available care time today (minutes)",
    min_value=1,
    max_value=300,
    value=st.session_state.owner.available_minutes
)

if st.button("Save owner info"):
    # Update the saved owner object in session state
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_minutes = int(available_minutes)

    st.success(f"Saved owner info for {owner_name}.")

st.divider()

# ---------------------------------------------------------
# Add Pet
# ---------------------------------------------------------

st.subheader("Add Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(pet_name, species)

    try:
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name}")
    except ValueError as error:
        st.error(str(error))

# Display current pets
pets = st.session_state.owner.get_pets()

if pets:
    st.write("Current pets:")

    pet_table = []

    for pet in pets:
        pet_table.append(
            {
                "Name": pet.name,
                "Species": pet.species,
                "Task Count": len(pet.get_tasks())
            }
        )

    st.table(pet_table)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------
# Add Task
# ---------------------------------------------------------

st.subheader("Add Care Task")

if not pets:
    st.info("Add a pet before creating tasks.")
else:
    pet_options = [pet.name for pet in pets]

    selected_pet_name = st.selectbox("Choose pet", pet_options)

    st.markdown("### Task Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input("Task title", value="Morning walk")

    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20
        )

    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    task_time = st.text_input("Time (24-hour HH:MM)", value="09:00")

    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        selected_pet = None

        for pet in pets:
            if pet.name == selected_pet_name:
                selected_pet = pet

        if selected_pet is None:
            st.error("Selected pet was not found.")
        else:
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                pet_name=selected_pet.name,
                time=task_time,
                frequency=frequency
            )

            try:
                selected_pet.add_task(new_task)
                st.success(f"Added task: {task_title} for {selected_pet.name}")
            except ValueError as error:
                st.error(str(error))

st.divider()

# ---------------------------------------------------------
# Current Tasks
# ---------------------------------------------------------

st.subheader("Current Tasks")

scheduler = Scheduler(st.session_state.owner)
tasks = scheduler.sort_tasks_by_time()

if tasks:
    task_table = []

    for task in tasks:
        task_table.append(
            {
                "Time": task.time,
                "Task": task.title,
                "Pet": task.pet_name,
                "Duration": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": task.completed
            }
        )

    st.table(task_table)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------
# Filter Tasks by Pet
# ---------------------------------------------------------

st.subheader("Filter Tasks by Pet")
st.caption("This section uses Scheduler.filter_tasks_by_pet().")

pets = st.session_state.owner.get_pets()

if not pets:
    st.info("Add a pet first to filter tasks.")
else:
    pet_options = [pet.name for pet in pets]
    selected_filter_pet = st.selectbox("Select a pet to view tasks", pet_options)

    if st.button("Filter by pet"):
        filtered_tasks = scheduler.filter_tasks_by_pet(selected_filter_pet)

        if not filtered_tasks:
            st.info(f"No tasks found for {selected_filter_pet}.")
        else:
            st.markdown(f"### Tasks for {selected_filter_pet}")

            filtered_table = []

            for task in filtered_tasks:
                filtered_table.append(
                    {
                        "Time": task.time,
                        "Task": task.title,
                        "Pet": task.pet_name,
                        "Duration": task.duration_minutes,
                        "Priority": task.priority,
                        "Frequency": task.frequency,
                        "Completed": task.completed
                    }
                )

            st.table(filtered_table)

st.divider()

# ---------------------------------------------------------
# Build Schedule
# ---------------------------------------------------------

st.subheader("Build Schedule")
st.caption("This button calls the Scheduler class from pawpal_system.py.")

if st.button("Generate schedule"):
    daily_plan = scheduler.generate_daily_plan()

    if not daily_plan:
        st.warning("No tasks could be scheduled.")
    else:
        st.markdown("### Today's Schedule")

        for task in daily_plan:
            st.markdown(
                f"""
**{task.time} - {task.title}**

Pet: {task.pet_name}  
Duration: {task.duration_minutes} minutes  
Priority: {task.priority}  
Frequency: {task.frequency}
"""
            )

        st.success(
            f"Generated a schedule using up to {st.session_state.owner.available_minutes} available minutes."
        )

st.divider()

# ---------------------------------------------------------
# Conflict Detection
# ---------------------------------------------------------

st.subheader("Check Conflicts")
st.caption("This checks for tasks scheduled at the exact same time.")

if st.button("Check for conflicts"):
    conflicts = scheduler.detect_conflicts()

    if not conflicts:
        st.success("No exact-time conflicts found.")
    else:
        st.warning("Conflicts found:")

        for task1, task2 in conflicts:
            st.write(
                f"{task1.time}: {task1.title} for {task1.pet_name} conflicts with "
                f"{task2.title} for {task2.pet_name}"
            )

st.divider()

# ---------------------------------------------------------
# Reset App
# ---------------------------------------------------------

if st.button("Reset app"):
    st.session_state.owner = Owner("Jordan", available_minutes=60)
    st.success("App reset successfully.")