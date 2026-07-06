# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.  Three core actions: feed pet, walk a pet, vet visits. 
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
Today's Schedule
================
- Morning Walk for Mochi at 08:00
- Feed Dinner for Mochi at 12:00
- Vet Reminder for Luna at 18:00

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
 ## python -m pytest
======================== test session starts =========================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\emili\PawPal\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 8 items                                                     

tests\test_pawpal.py ........                                   [100%]

========================= 8 passed in 0.07s ==========================

"Confidence Level 5/5"
## 📐 Smarter Scheduling

The scheduler now includes a few lightweight features to make pet-care planning easier to follow.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Orders tasks by their scheduled time in HH:MM format so the day plan is easier to read. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status or pet name to focus on a subset of work. |
| Conflict detection | `Scheduler.detect_conflicts()` and `Scheduler.conflict_warning()` | Flags tasks that share the same start time so obvious scheduling conflicts are visible. |
| Recurring task logic | `Task.mark_complete()` | When a daily or weekly task is marked complete, a new task instance is created for the next occurrence. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. **Enter owner details**: App launches with default owner "Jordan". Change name in "Owner Details" box if desired.
2. **Add pets**: Fill "New pet name", "age", "weight", "breed", "color", "mood" and click "Add pet". Repeat for multiple pets (e.g., Mochi, Thanos, Luna).
3. **Select pet to manage**: Use "Select pet to manage" dropdown to pick which pet to add tasks for. Selection persists across interactions.
4. **Add tasks**: Enter task "title" (e.g., "Morning walk"), "duration" in minutes, and "priority" level. Click "Add task" to assign to the selected pet.
5. **Generate schedule**: Click "Generate schedule" to build the daily plan. App sorts tasks by priority and time, displays them in a table. If conflicts exist (same start time), edit times in expandable sections to resolve them.
6. **Filter and view**: Use "Filter by pet" to focus on one pet's tasks, or "Show tasks" to see only pending/completed items. Tasks display in chronological order.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
