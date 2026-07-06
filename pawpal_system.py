from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Pet:
    name: str
    age: int
    weight: float
    breed: str
    color: str
    mood: str
    vitamins: List[str] = field(default_factory=list)
    vaccines: List[str] = field(default_factory=list)
    tasks: List["Task"] = field(default_factory=list)


@dataclass
class Task:
    title: str
    description: str
    priority: str
    duration_minutes: int
    pet: Optional[Pet] = None
    scheduled_time: Optional[str] = None
    completed: bool = False
    frequency: str = "once"
    due_date: Optional[date] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and create a new recurring task if needed."""
        self.completed = True
        if self.frequency == "daily":
            next_due_date = (self.due_date or date.today()) + timedelta(days=1)
            return Task(
                title=self.title,
                description=self.description,
                priority=self.priority,
                duration_minutes=self.duration_minutes,
                pet=self.pet,
                scheduled_time=self.scheduled_time,
                completed=False,
                frequency=self.frequency,
                due_date=next_due_date,
            )
        if self.frequency == "weekly":
            next_due_date = (self.due_date or date.today()) + timedelta(days=7)
            return Task(
                title=self.title,
                description=self.description,
                priority=self.priority,
                duration_minutes=self.duration_minutes,
                pet=self.pet,
                scheduled_time=self.scheduled_time,
                completed=False,
                frequency=self.frequency,
                due_date=next_due_date,
            )
        return None


@dataclass
class Owner:
    name: str
    address: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def add_pet_from_data(
        self,
        *, 
        name: str,
        age: int,
        weight: float,
        breed: str,
        color: str,
        mood: str,
    ) -> Pet:
        """Create and add a new pet from form-style data."""
        pet = Pet(name=name, age=age, weight=weight, breed=breed, color=color, mood=mood)
        self.add_pet(pet)
        return pet

    def add_task(self, pet: Pet, task: Task) -> None:
        """Attach a task to a specific pet."""
        task.pet = pet
        pet.tasks.append(task)


@dataclass
class Veterinary:
    health_info: str = "General pet health information"

    def schedule_dog_visit(self, pet: Pet, appointment_date: str) -> str:
        """Create a visit appointment for a pet."""
        return f"Scheduled visit for {pet.name} on {appointment_date}"

    def vaccines_for_dogs(self, pet: Pet) -> List[str]:
        """Return the pet's vaccine list."""
        return pet.vaccines

    def blood_test_for_dogs(self, pet: Pet) -> str:
        """Return a blood test recommendation for the pet."""
        return f"Blood test recommended for {pet.name}"

    def surgery_for_dogs(self, pet: Pet) -> str:
        """Return a surgery review message for the pet."""
        return f"Surgery review requested for {pet.name}"


class Scheduler:
    def build_plan(self, owner: Owner) -> List[Task]:
        """Build a prioritized plan from all tasks owned by the pets."""
        planned_tasks: List[Task] = []
        for pet in owner.pets:
            for task in pet.tasks:
                if task.scheduled_time is None:
                    task.scheduled_time = self._suggest_time(task)
                planned_tasks.append(task)
        return self.sort_by_time(sorted(planned_tasks, key=self._priority_rank))

    def explain_plan(self, tasks: List[Task]) -> str:
        """Return a simple text explanation of the planned tasks."""
        lines = []
        for task in tasks:
            pet_name = task.pet.name if task.pet else "unknown pet"
            lines.append(f"- {task.title} for {pet_name} at {task.scheduled_time}")
        return "\n".join(lines)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time in HH:MM format."""
        return sorted(
            tasks,
            key=lambda task: self._time_to_minutes(task.scheduled_time or self._suggest_time(task)),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        *,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion status or pet name."""
        filtered_tasks = list(tasks)
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed is completed]
        if pet_name is not None:
            pet_name_lower = pet_name.lower()
            filtered_tasks = [
                task for task in filtered_tasks if task.pet is not None and task.pet.name.lower() == pet_name_lower
            ]
        return filtered_tasks

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple[Task, Task]]:
        """Return pairs of tasks that share the same start time."""
        conflicts: List[tuple[Task, Task]] = []
        seen_times: dict[int, Task] = {}
        for task in tasks:
            start_time = self._time_to_minutes(task.scheduled_time or self._suggest_time(task))
            if start_time in seen_times:
                conflicts.append((seen_times[start_time], task))
            else:
                seen_times[start_time] = task
        return conflicts

    def conflict_warning(self, tasks: List[Task]) -> str:
        """Return a readable warning message for conflicting tasks."""
        conflicts = self.detect_conflicts(tasks)
        if not conflicts:
            return "No conflicts detected."
        details = []
        for first_task, second_task in conflicts:
            first_name = first_task.pet.name if first_task.pet else "unknown pet"
            second_name = second_task.pet.name if second_task.pet else "unknown pet"
            details.append(f"{first_task.title} ({first_name}) and {second_task.title} ({second_name})")
        return "Warning: conflicting tasks scheduled at the same time: " + "; ".join(details)

    def _suggest_time(self, task: Task) -> str:
        """Suggest a time slot based on task priority."""
        priority_map = {"high": "08:00", "medium": "12:00", "low": "18:00"}
        return priority_map.get(task.priority.lower(), "09:00")

    def _priority_rank(self, task: Task) -> tuple[int, int]:
        """Return a sort key for ordering tasks by priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return (priority_order.get(task.priority.lower(), 99), task.duration_minutes)

    def _time_to_minutes(self, time_value: str) -> int:
        """Convert an HH:MM string into minutes from midnight."""
        hours, minutes = map(int, time_value.split(":"))
        return hours * 60 + minutes
