# Smart Task Scheduling System with Priority, Dependencies, and Simulation.

## Overview

This project is a **Python-based task scheduling system** inspired by real-world production schedulers and CPU scheduling algorithms. It models how tasks are created, prioritized, dependency-checked, scheduled, and executed over simulated time.

The system is designed to be **modular, efficient, and analyzable**, making it suitable for both software engineering and data analysis use cases.

Key goals of the project:

* Practice **data structures & algorithms** (heaps, graphs, DFS)
* Model **realistic scheduling constraints**
* Enable **post-execution analysis** using CSV logs and Pandas

---

## Architecture

The system is composed of several clearly separated components:

```
Task        → Data model + validation
TaskManager → Storage + CSV persistence
Scheduler   → Priority-based task selection (heap)
DependencyManager → Dependency graph + cycle detection
DependencyAwareScheduler → Priority + dependency resolution
ExecutionSimulator → Event-driven execution simulation
```

Each component has a single responsibility, mirroring real-world system design.

---

## Core Features

### 1. Task Model

* Model tasks as individual objects and manage them through a separate system that provides fast access using hashmap.
* Each task is self-contained, validated at creation order via Class-Timeline, the manager provides a constant-time operation for adding retrieving and deleting task.


Each task contains:

* `task_id` (auto-generated)
* `priority` ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NEGLIGIBLE'], 
* `deadline` ['INTERNAL', 'EXTERNAL', 'HARD', 'SOFT'], 
* `duration` ['1', '2', '3', '4', '5'],
* `status` ['PENDING', 'ONGOING', 'COMPLETED'],
* `department`['HR', 'ENGINEERING', 'MARKETING', 'SALES', 'FINANCE', 'IT', 'CUSTOMER_SUPPORT'],
* `timeline` timeline is simply a timestamp when the task was created for tracing back.

Strict validation ensures only valid tasks are schedulable.

---

### 2. Priority-Based Scheduling



Tasks are scheduled using a **min-heap (`heapq`)** with the following ordering rules:

1. Priority (CRITICAL first)
2. Deadline type 
3. Creation time (FIFO)

This guarantees **O(log n)** insertion and removal.

Lazy deletion is used to avoid expensive heap rebuilds.

---

### 3. Dependency Management


Task dependencies are modeled as a **directed graph**:

* Nodes → tasks
* Edges → dependency relationships

Features:
* Among all tasks whose dependencies are satisfied, pick the highest priority one.
* Circular dependencies are detected early.
* Scheduler still uses **Heap Priority**.
* DFS-based cycle detection using a recursion stack.
* Indegree tracking for dependency resolution.
* Tasks become schedulable only when all prerequisites are completed.
* The Graph controls legality.
* This prevents duplucate scheduling and no deadlocks.

Time complexity: **O(V + E)**

---

### 4. Dependency-Aware Scheduling

The `DependencyAwareScheduler` combines:

* Priority scheduling
* Dependency resolution

When a task completes:

* Its dependent tasks have their indegree reduced
* Newly unlocked tasks are pushed into the scheduler heap

This mirrors real-world job pipelines and build systems.

---

### 5. Execution Simulation

The `ExecutionSimulator` runs an **event-driven simulation** of task execution.

It tracks:

* Execution order
* Start and end times
* Idle time
* Missed deadlines

Instead of advancing time step-by-step, the simulator jumps directly between events, improving realism and efficiency.

---

### 6. CSV Logging & Analysis

All task states are written to CSV files for later analysis.

This enables:

* Performance analysis with Pandas
* Deadline violation statistics
* Scheduler strategy comparisons

The design intentionally preserves historical records for data analysis.

---

## Example Workflow

1. Create tasks
2. Register them with the `TaskManager`
3. Define dependencies
4. Validate the dependency graph (cycle check)
5. Load tasks into the dependency-aware scheduler
6. Execute tasks or simulate execution
7. Analyze results via CSV logs

---

## Algorithms & Data Structures Used

* Hash maps (`dict`) for O(1) access
* Min-heaps (`heapq`) for priority scheduling
* Directed graphs (adjacency lists)
* DFS with recursion stack for cycle detection
* Event-driven simulation

---

## Complexity Summary

| Operation             | Complexity        |
| --------------------- | ----------------- |
| Add task              | O(1)              |
| Schedule task         | O(log n)          |
| Dependency validation | O(V + E)          |
| Task execution        | O(log n) per task |

---

## Possible Extensions

* Replace CSV with SQLite for scalability.
* Support task preemption.
* Visualize execution timelines.

---

## Motivation

This project was built to explore **how real scheduling systems work under constraints**, combining algorithmic correctness with practical design tradeoffs.

It intentionally balances clarity, performance, and extensibility.

---

## Author

Created as a systems-oriented Python project for learning and experimentation.

---

## License

MIT License
