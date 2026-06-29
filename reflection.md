# PawPal+ Project Reflection

## 1. System Design
The user needs to be able to enter pet info, generate daily schedules, and add tasks.

We would need a pet object with attributes : name, species, breed, age, and methods : update_profile(). We would need a task object with attributes : name, duration, recurrence, and is_completed, and methods : update_task(), mark_complete(). We would need a user object with attributes : name, start_time, end_time, and methods : update_availability(). We would need a schedule object with attributes : date, tasks_scheduled, and methods : add_task.

**a. Initial design**

- Briefly describe your initial UML design.

The system is designed around 4 core classes which are Owner, Pet, Task, and Scheduler. The Owner class represents the user of the application and connects to one or more pets. The Pet class represents individual animals. The Task class represents individual pet care activities like feeding, walking, and grooming. The Scheduler class is the main logic.

- What classes did you include, and what responsibilities did you assign to each?

The Owner class stores information such as name, contact details, available daily time, and preferences. It is responsible for managing pets and providing scheduling constraints. The Pet class contains basic attributes like name, species, breed, and age. Each pet has a list of tasks such as feeding, walking, and grooming. The Task class represents individual pet care activities. Each task includes details such as title, duration, priority, category, and whether it is required. The Scheduler class takes an owner and a list of tasks, then generates a daily plan based on constraints like available time and task priority. It is responsible for sorting, filtering, and organizing tasks into a structures schedule. 



**b. Design changes**

- Did your design change during implementation?

Yes, the design changed after reviewing AI feedback.

- If yes, describe at least one change and why you made it.

One key change was clarifying the data flow between components. Initially, tasks were stored inside each pet, while the scheduler also maintained a separate task pool. This created a potential duplication issue, so the design was adjusted so that the Scheduler dynamically collects tasks from all pets instead of relying on a separate stored list. Another improvement was recognizing missing relationships and structure details. The design was updated to consider linking Pet back to its Owner, and to ensure that tasks could optionally reference their associated pet to trace them better. Another one was the need for a more complete DailyPlan structure. It was updated conceptually to include scheduled tasks and summary information so that the output of the scheduler is meaningful and usable in the UI.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
