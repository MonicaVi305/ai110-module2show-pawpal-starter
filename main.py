from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Jordan", address="123 Pet Street", phone="555-0100")

    dog = Pet(name="Mochi", age=3, weight=12.5, breed="Labrador", color="Golden", mood="Happy")
    cat = Pet(name="Luna", age=2, weight=7.2, breed="Siamese", color="White", mood="Calm")
    owner.add_pet(dog)
    owner.add_pet(cat)

    owner.add_task(dog, Task(title="Morning Walk", description="Walk around the park", priority="high", duration_minutes=30, scheduled_time="16:00"))
    owner.add_task(dog, Task(title="Feed Dinner", description="Serve dinner", priority="medium", duration_minutes=10, scheduled_time="08:30"))
    owner.add_task(cat, Task(title="Vet Reminder", description="Give medicine", priority="low", duration_minutes=15, scheduled_time="12:15"))
    owner.add_task(cat, Task(title="Play Session", description="Play time", priority="medium", duration_minutes=20, scheduled_time="08:30"))
    medicine_task = Task(title="Give Vitamins", description="Daily vitamins", priority="high", duration_minutes=5, scheduled_time="07:30", frequency="daily")
    owner.add_task(dog, medicine_task)

    scheduler = Scheduler()
    plan = scheduler.build_plan(owner)
    incomplete_tasks = scheduler.filter_tasks(plan, completed=False)
    mochi_tasks = scheduler.filter_tasks(plan, pet_name="Mochi")
    conflicts = scheduler.detect_conflicts(plan)

    print("Today's Schedule")
    print("================")
    for task in incomplete_tasks:
        print(f"- {task.title} for {task.pet.name if task.pet else 'unknown pet'} at {task.scheduled_time}")

    print("\nMochi tasks:")
    for task in mochi_tasks:
        print(f"- {task.title} at {task.scheduled_time}")

    if conflicts:
        print("\nConflicts detected:")
        for first_task, second_task in conflicts:
            print(f"- {first_task.title} and {second_task.title} overlap")
    else:
        print("\nNo conflicts detected")

    print("\nConflict warning:")
    print(scheduler.conflict_warning(plan))

    recurring_task = medicine_task.mark_complete()
    if recurring_task is not None:
        owner.add_task(dog, recurring_task)
        print("\nAdded next recurring task:")
        print(f"- {recurring_task.title} for {recurring_task.pet.name if recurring_task.pet else 'unknown pet'} on {recurring_task.due_date}")


if __name__ == "__main__":
    main()
