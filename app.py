import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", address="Unknown", phone="Unknown")

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app now stores an Owner object in session state so your pet care data persists while you navigate.
"""
) 

st.subheader("Owner Details")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

st.subheader("Add a New Pet")
new_pet_name = st.text_input("New pet name", key="new_pet_name")
new_pet_age = st.number_input("New pet age", min_value=0, max_value=30, value=1, key="new_pet_age")
new_pet_weight = st.number_input("New pet weight (kg)", min_value=0.1, max_value=100.0, value=5.0, step=0.1, key="new_pet_weight")
new_pet_breed = st.text_input("New pet breed", value="Mixed", key="new_pet_breed")
new_pet_color = st.text_input("New pet color", value="Brown", key="new_pet_color")
new_pet_mood = st.text_input("New pet mood", value="Happy", key="new_pet_mood")

if st.button("Add pet"):
    owner.add_pet_from_data(
        name=new_pet_name,
        age=int(new_pet_age),
        weight=float(new_pet_weight),
        breed=new_pet_breed,
        color=new_pet_color,
        mood=new_pet_mood,
    )
    st.success(f"Added {new_pet_name} to {owner.name}'s pets.")
 
if not owner.pets:
    owner.add_pet(Pet(name="Mochi", age=3, weight=12.5, breed="dog", color="golden", mood="happy"))

if "selected_pet_index" not in st.session_state:
    st.session_state.selected_pet_index = 0

pet_index = st.selectbox(
    "Select pet to manage",
    list(range(len(owner.pets))),
    format_func=lambda i: owner.pets[i].name,
    index=st.session_state.selected_pet_index,
)
st.session_state.selected_pet_index = pet_index
active_pet = owner.pets[pet_index]

st.markdown("### Tasks")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    owner.add_task(
        active_pet,
        Task(
            title=task_title,
            description=f"{priority} priority task",
            priority=priority,
            duration_minutes=int(duration),
        ),
    )

scheduler = Scheduler()
all_tasks = [task for pet_item in owner.pets for task in pet_item.tasks]
pet_options = ["All"] + [pet_item.name for pet_item in owner.pets]
filter_pet = st.selectbox("Filter by pet", pet_options)
status_filter = st.selectbox("Show tasks", ["All", "Pending", "Completed"])

completed_value = None
if status_filter == "Completed":
    completed_value = True
elif status_filter == "Pending":
    completed_value = False

filtered_tasks = scheduler.filter_tasks(
    all_tasks,
    completed=completed_value,
    pet_name=None if filter_pet == "All" else filter_pet,
)
 
sorted_tasks = scheduler.sort_by_time(filtered_tasks)

if sorted_tasks:
    st.write("Current tasks:")
    task_rows = [
        {
            "pet": task.pet.name if task.pet else "unknown",
            "title": task.title,
            "priority": task.priority,
            "duration": task.duration_minutes,
            "time": task.scheduled_time or "TBD",
            "status": "Done" if task.completed else "Pending",
        }
        for task in sorted_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks match the current filters.")

st.divider()
 
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    st.session_state.current_plan = scheduler.build_plan(owner)

if "current_plan" in st.session_state:
    plan = st.session_state.current_plan
    conflict_message = scheduler.conflict_warning(plan)
    conflicts = scheduler.detect_conflicts(plan)

    if conflicts:
        st.warning(f"⚠️ {conflict_message}")
        st.write("**Resolve conflicts by editing task times:**")
        
        for idx, (task1, task2) in enumerate(conflicts):
            with st.expander(f"Conflict {idx + 1}: {task1.title} & {task2.title} both at {task1.scheduled_time}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{task1.pet.name}'s {task1.title}**")
                    new_time_1 = st.text_input(
                        f"New time for {task1.title}",
                        value=task1.scheduled_time or "08:00",
                        key=f"conflict_time_{idx}_task1",
                    )
                    if st.button(f"Update {task1.title}", key=f"update_btn_{idx}_task1"):
                        task1.scheduled_time = new_time_1
                        st.success(f"Updated {task1.title} to {new_time_1}")
                        st.rerun()
                
                with col2:
                    st.write(f"**{task2.pet.name}'s {task2.title}**")
                    new_time_2 = st.text_input(
                        f"New time for {task2.title}",
                        value=task2.scheduled_time or "09:00",
                        key=f"conflict_time_{idx}_task2",
                    )
                    if st.button(f"Update {task2.title}", key=f"update_btn_{idx}_task2"):
                        task2.scheduled_time = new_time_2
                        st.success(f"Updated {task2.title} to {new_time_2}")
                        st.rerun()
    else:
        st.success(f"✅ {conflict_message}")

    st.subheader("Today's Schedule")
    schedule_display = scheduler.sort_by_time(plan)
    
    if schedule_display:
        schedule_rows = [
            {
                "pet": task.pet.name if task.pet else "unknown",
                "title": task.title,
                "priority": task.priority,
                "time": task.scheduled_time or "TBD",
                "duration": task.duration_minutes,
                "status": "✓ Done" if task.completed else "⏳ Pending",
            }
            for task in schedule_display
        ]
        st.table(schedule_rows)
    else:
        st.info("No tasks in the schedule.")
    schedule_rows = [
        {
            "pet": task.pet.name if task.pet else "unknown pet",
            "title": task.title,
            "time": task.scheduled_time or "TBD",
            "priority": task.priority,
        }
        for task in plan
    ]
    st.table(schedule_rows)
