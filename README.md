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
* `timeline` is simply a timestamp when the task was created for tracing back.

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

# 🧪 Unit Test Suite – Task Scheduling System.

## Overview.

This module contains a **comprehensive unit and integration test suite** for the Task Scheduling System. It validates correctness, stability, and expected behavior across all major components:

* Task creation and validation
* Task management and persistence
* Priority-based scheduling
* Dependency handling and cycle detection
* Dependency-aware scheduling
* Event-driven execution simulation

The tests are written using Python’s built-in `unittest` framework and are designed to be **deterministic, isolated, and repeatable**.

---

## Purpose of This Test Suite.

The test suite serves four main purposes:

1. **Verify correctness** of individual components (unit tests)
2. **Validate interactions** between components (integration tests)
3. **Prevent regressions** during refactoring or optimization
4. **Document system behavior** through executable examples

Importantly, these tests **do not modify production code** — they only assert expected outcomes.

---

## Test Environment Setup

### Global Timeline Reset

Many tests reset the class-level counter:

```python
Task.global_timeline = 0
```

This ensures:

* Predictable task IDs
* Deterministic test results
* Isolation between tests

### Filesystem Cleanup

Before testing CSV output, the test suite removes existing directories:

```python
shutil.rmtree("task_records")
```

This prevents false positives caused by leftover files from previous runs.

---

## Test Modules Explained.

---

## `TestTask`

### What It Tests.

* Valid task creation
* Auto-generated task IDs
* Input validation (priority, department)

### Why It Matters.

This ensures the **core data model is safe and strict**. Invalid tasks are rejected early, preventing corrupted schedules downstream.

---

## `TestTaskManager`

### What It Tests.

* Adding and retrieving tasks
* Duplicate task ID protection
* Task status updates
* CSV file creation

### Why It Matters.

This validates:

* O(1) task access via hash maps
* Persistence of task state
* Historical record keeping for later data analysis

---

## `TestScheduler`

### What It Tests.

* Priority ordering using a heap
* Lazy deletion of tasks

### Why It Matters.

Confirms that:

* High-priority tasks are always selected first
* Deleted tasks are never executed
* Heap-based scheduling remains efficient and correct

---

## `TestDependencyManager`

### What It Tests.

* Valid dependency graphs (DAGs)
* Cycle detection using DFS

### Why It Matters.

This prevents:

* Deadlocks
* Infinite scheduling loops
* Invalid execution plans

Cycle detection runs in **O(V + E)** time.

---

## `TestDependencyAwareScheduler`

### What It Tests.

* Blocking of dependent tasks
* Automatic unlocking of tasks after completion

### Why It Matters.

Validates the **integration of priority scheduling and dependency resolution**, mirroring real-world job pipelines and build systems.

---

## `TestExecutionSimulator`

### What It Tests.

* Full execution of tasks
* Status transitions to COMPLETED
* Execution logging

### Why It Matters.

Confirms the correctness of the **event-driven execution model**, ensuring:

* Time advances correctly
* Tasks complete as expected
* Execution history is recorded for analysis

---

## Test Coverage Summary

| Component                  | Covered |
| -------------------------- | ------- |
| Task model                 | ✅       |
| TaskManager                | ✅       |
| Priority scheduler         | ✅       |
| Dependency graph           | ✅       |
| Dependency-aware scheduler | ✅       |
| Execution simulator        | ✅       |

This suite tests both **individual units** and **end-to-end behavior**.

---

## How to Run the Tests.

From the project root:

```bash
python -m unittest
```

Or run a specific test file:

```bash
python -m unittest test_scheduler.py
```

---

## Design Philosophy

These tests are intentionally:

* **Black-box oriented** – verify outcomes, not implementation details
* **Deterministic** – same input always yields same result
* **Side-effect aware** – file system and state are explicitly managed

Together, they provide strong confidence in the system’s correctness and make future changes safe.

---

## Conclusion

This test suite elevates the project from a working prototype to a **reliable, maintainable system**. It demonstrates a solid understanding of:

* Software correctness
* Algorithm validation
* Integration testing
* Defensive programming

Well-tested systems are trustworthy systems — this suite ensures exactly that.

