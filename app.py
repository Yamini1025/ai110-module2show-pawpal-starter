import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# Ensure owner object exists in session_state
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Jordan", contact_info="jordan@example.com", available_minutes_per_day=240)

owner: Owner = st.session_state["owner"]

st.write(f"Owner: {owner.name}")
if st.button("Add example pet & tasks"):
    pet = Pet(name="Mochi", species="cat")
    owner.add_pet(pet)
    pet.add_task(Task(title="Play", duration_minutes=20, priority="low"))
    pet.add_task(Task(title="Groom", duration_minutes=15, priority="medium"))
    st.success("Added pet and tasks to owner in session_state")

if st.button("Show schedule"):
    scheduler = Scheduler(owner=owner, day_start=8, day_end=18)
    plan = scheduler.generate_daily_plan()
    st.text(scheduler.explain_plan(plan))

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Use the Owner stored in session_state to build a schedule
    owner = st.session_state.get("owner")
    if not owner:
        st.error("No owner found in session; please create or load an owner first.")
    else:
        scheduler = Scheduler(owner=owner, day_start=8, day_end=18)
        plan = scheduler.generate_daily_plan()
        st.text(scheduler.explain_plan(plan))
    
st.subheader("Add a Pet")

# assumes `owner` is already in st.session_state (see earlier example)
with st.form("add_pet_form"):
    new_name = st.text_input("Pet name", value="")
    new_species = st.selectbox("Species", ["dog", "cat", "other"])
    new_breed = st.text_input("Breed (optional)", value="")
    new_age = st.number_input("Age", min_value=0, max_value=50, value=1)
    submitted = st.form_submit_button("Add Pet")

if submitted:
    pet = Pet(
        name=new_name or "Unnamed",
        species=new_species,
        breed=new_breed or None,
        age=int(new_age),
    )
    owner.add_pet(pet)
    st.success(f"Added pet: {pet.name}")

st.markdown("**Current pets**")
if owner.pets:
    pets_table = [
        {"name": p.name, "species": p.species, "breed": p.breed or "", "age": p.age}
        for p in owner.pets
    ]
    st.table(pets_table)
else:
    st.info("No pets yet. Use the form above to add one.")