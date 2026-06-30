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

1. Read the scenario carefully and identify requirements and edge cases.
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
Daily plan:
- 08:00 - 08:45: Morning walk
- 08:45 - 08:55: Medication reminder
- 08:55 - 09:25: Play session

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

## 📐 Smarter Scheduling

This project includes a few simple scheduling features that help PawPal+ choose better pet care tasks.

- **Task sorting** (`Scheduler.sort_by_time`, `Scheduler.sort_tasks_by_priority`)
  - `sort_by_time()` orders tasks by the owner's preferred start time, then by priority and duration.
  - `sort_tasks_by_priority()` puts higher-priority tasks first so important care items are scheduled earlier.

- **Filtering** (`Scheduler.filter_tasks_by_completion`, `Scheduler.filter_tasks_by_pet_name`)
  - `filter_tasks_by_completion()` keeps only tasks that match the requested completion status, so completed tasks are skipped when building a plan.
  - `filter_tasks_by_pet_name()` keeps only tasks for a specific pet, which helps when the owner wants a single pet's schedule.

- **Conflict detection** (`Scheduler.detect_conflicts`)
  - `detect_conflicts()` checks for tasks with overlapping preferred times or the same preferred start time for the same pet and returns warnings.

- **Recurring task logic** (`Task.mark_complete` recurrence)
  - When a recurring task is marked complete, `mark_complete()` creates the next occurrence for the future date, so daily or weekly tasks keep repeating.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
