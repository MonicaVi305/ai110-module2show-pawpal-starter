import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion_marks_status() -> None:
    task = Task(title="Morning walk", description="Walk around the park", priority="high", duration_minutes=30)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    owner = Owner(name="Jordan", address="123 Pet Street", phone="555-0100")
    pet = Pet(name="Mochi", age=3, weight=12.5, breed="Labrador", color="Golden", mood="Happy")
    owner.add_pet(pet)

    initial_count = len(pet.tasks)
    task = Task(title="Feed dinner", description="Serve dinner", priority="medium", duration_minutes=10)

    owner.add_task(pet, task)

    assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_orders_tasks_by_time() -> None:
    scheduler = Scheduler()
    first_task = Task(title="Later", description="", priority="low", duration_minutes=10, scheduled_time="16:00")
    second_task = Task(title="Earlier", description="", priority="low", duration_minutes=10, scheduled_time="08:00")

    ordered_tasks = scheduler.sort_by_time([first_task, second_task])

    assert [task.title for task in ordered_tasks] == ["Earlier", "Later"]


def test_filter_tasks_by_pet_name() -> None:
    scheduler = Scheduler()
    pet = Pet(name="Mochi", age=3, weight=12.5, breed="Labrador", color="Golden", mood="Happy")
    task_one = Task(title="Walk", description="", priority="high", duration_minutes=20, pet=pet)
    task_two = Task(title="Feed", description="", priority="medium", duration_minutes=10, pet=None)

    filtered_tasks = scheduler.filter_tasks([task_one, task_two], pet_name="Mochi")

    assert filtered_tasks == [task_one]


def test_detect_conflicts_reports_same_start_time() -> None:
    scheduler = Scheduler()
    pet = Pet(name="Mochi", age=3, weight=12.5, breed="Labrador", color="Golden", mood="Happy")
    first_task = Task(title="Walk", description="", priority="high", duration_minutes=20, pet=pet, scheduled_time="08:30")
    second_task = Task(title="Feed", description="", priority="medium", duration_minutes=10, pet=pet, scheduled_time="08:30")

    conflicts = scheduler.detect_conflicts([first_task, second_task])

    assert conflicts == [(first_task, second_task)]
