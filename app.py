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

pet = owner.pets[0]
pet_name = st.text_input("Pet name", value=pet.name)
if pet_name != pet.name:
    pet.name = pet_name

species = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(pet.breed) if pet.breed in ["dog", "cat", "other"] else 0)
if species != pet.breed:
    pet.breed = species

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
        pet,
        Task(
            title=task_title,
            description=f"{priority} priority task",
            priority=priority,
            duration_minutes=int(duration),
        ),
    )

all_tasks = [task for pet_item in owner.pets for task in pet_item.tasks]
if all_tasks:
    st.write("Current tasks:")
    task_rows = [
        {"pet": task.pet.name if task.pet else pet.name, "title": task.title, "priority": task.priority, "duration": task.duration_minutes}
        for task in all_tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.build_plan(owner)
    st.success("Today's Schedule")
    for task in plan:
        pet_name_for_task = task.pet.name if task.pet else "unknown pet"
        st.write(f"- {task.title} for {pet_name_for_task} at {task.scheduled_time}")
