import unittest
import os
import shutil



# Example Usage:

# manager = TaskManager()
# dependency = DependencyManager()
# schedule = Scheduler()
# scheduler = DependencyAwareScheduler(dependency)

# 1. Create tasks
# t1 = Task(priority='HIGH', deadline='HARD', duration=3, status='PENDING', department='FINANCE')
# t2 = Task(priority='LOW', deadline='INTERNAL', duration=2, status='PENDING', department='HR')
# t3 = Task(priority='MEDIUM', deadline='EXTERNAL', duration=4, status='PENDING', department='ENGINEERING')

# 2. Store tasks
# manager.add_task(t1)
# manager.add_task(t2)
# manager.add_task(t3)

# 3. Register tasks in dependency graph
# dependency.add_task(t1.task_id)
# dependency.add_task(t2.task_id)
# dependency.add_task(t3.task_id)

# 4. Add dependencies
# dependency.add_dependency(t1.task_id, t3.task_id)

# 5. Validate DAG
# # Cycle check (MANDATORY)
# # No cycle → continue.
# if dependency.has_cycle_dfs():
#     raise RuntimeError("Circular dependency detected")

# 6. Initialize correct scheduler
# scheduler = DependencyAwareScheduler(dependency)

# 7. INITIAL DEPENDENCY-AWARE LOAD
# for task in manager.tasks.values():
#     scheduler.add_task_if_ready(task)

# 8. Normal execution
# next_task = scheduler.pop_next_task()
# scheduler.complete_task(next_task, manager)

# print(scheduler.peek_next_task())




# Import everything from your project file
# Rename "project" to the actual filename (without .py)
from smart_task_scheduler import (
    Task,
    TaskManager,
    Scheduler,
    DependencyManager,
    DependencyAwareScheduler,
    ExecutionSimulator
)

class TestTask(unittest.TestCase):

    def setUp(self):
        # Reset global timeline before each test
        Task.global_timeline = 0

    def test_task_creation_valid(self):
        task = Task(
            priority="HIGH",
            deadline="HARD",
            duration=3,
            status="PENDING",
            department="FINANCE"
        )

        self.assertEqual(task.priority, "HIGH")
        self.assertEqual(task.department, "FINANCE")
        self.assertTrue(task.task_id.startswith("T01"))

    def test_task_invalid_priority(self):
        with self.assertRaises(ValueError):
            Task(
                priority="URGENT",
                deadline="HARD",
                duration=3,
                status="PENDING",
                department="FINANCE"
            )

    def test_task_invalid_department(self):
        with self.assertRaises(ValueError):
            Task(
                priority="HIGH",
                deadline="HARD",
                duration=3,
                status="PENDING",
                department="LEGAL"
            )


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        Task.global_timeline = 0
        self.manager = TaskManager()

        # Clean CSV directory if it exists
        if os.path.isdir("task_records"):
            shutil.rmtree("task_records")

    def test_add_and_get_task(self):
        task = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        self.manager.add_task(task)

        fetched = self.manager.get_task(task.task_id)
        self.assertEqual(fetched, task)

    def test_duplicate_task_id(self):
        task = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        self.manager.add_task(task)

        with self.assertRaises(KeyError):
            self.manager.add_task(task)

    def test_update_task_status(self):
        task = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        self.manager.add_task(task)

        self.manager.update_task(task.task_id, "COMPLETED")
        self.assertEqual(task.status, "COMPLETED")

    def test_csv_written(self):
        task = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        self.manager.add_task(task)

        self.assertTrue(os.path.isfile("task_records/task.csv"))


class TestScheduler(unittest.TestCase):

    def setUp(self):
        Task.global_timeline = 0
        self.scheduler = Scheduler()

    def test_priority_ordering(self):
        t1 = Task("LOW", "SOFT", 2, "PENDING", "HR")
        t2 = Task("CRITICAL", "INTERNAL", 1, "PENDING", "IT")

        self.scheduler.add_task(t1)
        self.scheduler.add_task(t2)

        next_task = self.scheduler.pop_next_task()
        self.assertEqual(next_task, t2)

    def test_lazy_delete(self):
        task = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        self.scheduler.add_task(task)

        self.scheduler.delete_task(task.task_id)
        self.assertIsNone(self.scheduler.pop_next_task())


class TestDependencyManager(unittest.TestCase):

    def setUp(self):
        self.dependency = DependencyManager()

    def test_no_cycle(self):
        self.dependency.add_task("A")
        self.dependency.add_task("B")
        self.dependency.add_dependency("A", "B")

        self.assertFalse(self.dependency.has_cycle_dfs())

    def test_cycle_detection(self):
        self.dependency.add_task("A")
        self.dependency.add_task("B")
        self.dependency.add_dependency("A", "B")
        self.dependency.add_dependency("B", "A")

        self.assertTrue(self.dependency.has_cycle_dfs())


class TestDependencyAwareScheduler(unittest.TestCase):

    def setUp(self):
        Task.global_timeline = 0
        self.manager = TaskManager()
        self.dependency = DependencyManager()
        self.scheduler = DependencyAwareScheduler(self.dependency)

    def test_dependency_blocks_execution(self):
        t1 = Task("HIGH", "HARD", 3, "PENDING", "FINANCE")
        t2 = Task("LOW", "SOFT", 2, "PENDING", "HR")

        self.manager.add_task(t1)
        self.manager.add_task(t2)

        self.dependency.add_task(t1.task_id)
        self.dependency.add_task(t2.task_id)
        self.dependency.add_dependency(t1.task_id, t2.task_id)

        self.scheduler.add_task_if_ready(t1)
        self.scheduler.add_task_if_ready(t2)

        first = self.scheduler.pop_next_task()
        self.assertEqual(first, t1)

        self.scheduler.complete_task(first, self.manager)
        second = self.scheduler.pop_next_task()
        self.assertEqual(second, t2)


class TestExecutionSimulator(unittest.TestCase):

    def setUp(self):
        Task.global_timeline = 0
        self.manager = TaskManager()
        self.dependency = DependencyManager()
        self.scheduler = DependencyAwareScheduler(self.dependency)

    def test_execution_completes_tasks(self):
        t1 = Task("HIGH", "HARD", 2, "PENDING", "FINANCE")
        self.manager.add_task(t1)

        self.dependency.add_task(t1.task_id)
        self.scheduler.add_task_if_ready(t1)

        simulator = ExecutionSimulator(self.scheduler)
        simulator.run(self.manager)

        self.assertEqual(t1.status, "COMPLETED")
        self.assertEqual(len(simulator.execution_log), 1)


if __name__ == "__main__":
    unittest.main()

# to run tests: 
# python -m unittest test_scheduler.py