# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Skeleton design:

```python
from dataclasses import dataclass, field
from typing import List

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

@dataclass
class Task:
    title: str
    description: str
    priority: str
    duration_minutes: int
    scheduled_time: str | None = None

@dataclass
class Owner:
    name: str
    address: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def feed_dog(self, pet: Pet, frequency: str, quantity: str, food_type: str) -> None:
        pass

    def walk_dog(self, pet: Pet, frequency: str, time_of_day: str, place: str) -> None:
        pass

    def play_time(self, pet: Pet) -> None:
        pass

    def vet_visit(self, pet: Pet) -> None:
        pass

@dataclass
class Veterinary:
    health_info: str

    def schedule_dog_visit(self, pet: Pet, appointment_date: str) -> None:
        pass

    def vaccines_for_dogs(self, pet: Pet) -> None:
        pass

    def blood_test_for_dogs(self, pet: Pet) -> None:
        pass

    def surgery_for_dogs(self, pet: Pet) -> None:
        pass
```

Core actions represented in the skeleton:
1. Feed pet: frequency, quantity, and food type.
2. Walk a pet: frequency, time, and place.
3. Give medicine: vitamins and medicines.
4. Vet visits: vaccines, regular appointments, vitamins, medicines, blood tests, and next visit tracking.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

A clean structure would be:
1. Dataclasses for Pet, Owner, Task
2. A Scheduler or Planner class for building the plan
3. A simple output object or list of scheduled items for the final plan
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a lightweight conflict check that only warns when two tasks share the same start time. This is simpler and easier to read than a full overlap-duration model, and it is reasonable for this starter app because the main goal is to surface obvious scheduling issues quickly.

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
