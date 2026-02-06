# Milestone 1: Basic Task Management
# Objective: Build the core data model.
# Tasks
# 1) Define a Task class:
#     * task_id
#     * priority
#     * deadline
#     * duration
# 2) Store tasks using a Hash Map (task_id → Task)

# DSA Focus:
# I) Hash Tables.
# II) Object modeling.

# Interview Angle: 
# Why did you choose a hash map over a list for task storage? Dictionary are easy to access, while lists require a linear search as the number of tasks increases.
# Why you used a counter? I used a class-level counter to represent a timeline because task creation order is a global property shared across all tasks, not something unique to a single instance.


#task_id={}, 
#priority = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NEGLIGIBLE'], 
#deadline = ['INTERNAL', 'EXTERNAL', 'HARD', 'SOFT'], 
#duration = ['1', '2', '3', '4', '5']
#time_line = timeline is simply a timestamp when the task was created so we can trace back.
#status = ['PENDING', 'ONGOING', 'COMPLETED']
#department = ['HR', 'ENGINEERING', 'MARKETING', 'SALES', 'FINANCE', 'IT', 'CUSTOMER_SUPPORT']



from multiprocessing import heap
import os 
import heapq
import sys
import csv
from collections import defaultdict, deque

print('Python version:', sys.version)

class Task:
    # Milestone 1: Basic Task Management.
    # I. Task data model with validation.
    # II. Auto-generated Task ID based on timeline, department, and priority.
    # III. Class-level timeline counter.  
        

    global_timeline = 0
    #Task.deleted = False
    
    PRIORITY_CODES = {
        'CRITICAL': 'C',
        'HIGH': 'H',
        'MEDIUM': 'M',
        'LOW': 'L',
        'NEGLIGIBLE': 'N'
    }
    DEPARTMENT_CODES = {
        'HR': 'HR',
        'ENGINEERING': 'EN',
        'MARKETING': 'MR',
        'SALES': 'SL',
        'FINANCE': 'FI',
        'IT': 'IT',
        'CUSTOMER_SUPPORT': 'CS',
        'GENERAL': 'G'
    }


    def __init__(self, priority, deadline, duration, status, department, task_id=None):

        self.department = department if department is not None else 'GENERAL'
        self.priority = priority if priority is not None else 'NEGLIGIBLE'
        self.deadline = deadline if deadline is not None else 'SOFT'
        self.duration = duration if duration is not None else 5
        self.status = status if status is not None else 'PENDING'
        

        # Validation
        if self.department not in ['HR', 'ENGINEERING', 'MARKETING', 'SALES', 'FINANCE', 'IT', 'CUSTOMER_SUPPORT']:
            raise ValueError("INVALID DEPARTMENT VALUE")

        if self.priority not in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NEGLIGIBLE']:
            raise ValueError("INVALID PRIORITY VALUE")
        
        if self.deadline not in ['INTERNAL', 'EXTERNAL', 'HARD', 'SOFT']:
            raise ValueError("INVALID DEADLINE VALUE")
        
        if self.duration not in [1, 2, 3, 4, 5]:
            raise ValueError("INVALID DURATION VALUE")
        
        if self.status not in ['PENDING', 'ONGOING', 'COMPLETED']:
            raise ValueError("INVALID STATUS VALUE")

        # Timeline handling
        Task.global_timeline += 1
        self.time_line = Task.global_timeline

        # Auto-generated Task ID based on timeline, department, and priority
        dept_code = Task.DEPARTMENT_CODES[self.department]
        self.task_id = f"T{self.time_line:02d}{dept_code}"

        # Lazy deletion flag (Scheduler uses this)
        #The flag (Scheduler) should exist for every valid task
        #Validation should happen before the task is considered schedulable.
        self.deleted = False

    def __repr__(self):

        return (
            f"Task(TASK_ID={self.task_id},"
            f"DEPARTMENT={self.department},"
            f"PRIORITY={self.priority},"
            f"DEADLINE={self.deadline},"
            f"DURATION={self.duration},"
            f"TIMELINE={self.time_line}, "
            f"STATUS={self.status})"
        )
        

class TaskManager:
    # Milestone 1: Basic Task Management
    # I. Stores tasks in a hash map for O(1) access.
    # II. Exports task data to CSV for analysis.    
    def __init__(self):
        # Stores tasks in O(1) lookup time
        # Writes a full snapshot of tasks to CSV
        self.tasks = {}


    def add_task(self, task):
        # Checks for duplicate task ID
        # Stores task in dictionary
        # Calls record_csv()
        if task.task_id in self.tasks:
            raise KeyError(f"Task ID {task.task_id} already exists")
        self.tasks[task.task_id] = task
        self.record_csv() # record after adding

    def record_csv(self, filename="task.csv"):
        # Creates task_records/ directory if needed
        # Writes all tasks sorted by timeline
        headers = ['timeline', 'task_id', 'department', 'priority', 'deadline', 'duration', 'status']
        
        # Check if the folders exists, if not create one where to store the csv files containing task records.
        if os.path.isdir('task_records') is False:
            os.mkdir('task_records')
            
        working_dir = os.path.join(os.getcwd(), 'task_records')
        with open(f"{working_dir}/{filename}", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            # Write each task as a row
            for task in sorted(self.tasks.values(), key=lambda t: t.time_line):
                writer.writerow({
                    'timeline': task.time_line,
                    'task_id': task.task_id,
                    'department': task.department,
                    'priority': task.priority,
                    'deadline': task.deadline,
                    'duration': task.duration,
                    'status': task.status
                })

    def update_task(self, task_id, new_status):
        if task_id not in self.tasks:
            raise KeyError(f"Task ID {task_id} not found")
    
        if new_status not in ['PENDING', 'ONGOING', 'COMPLETED']:
                raise ValueError(f"Invalid status: {new_status}")
    
        self.tasks[task_id].status = new_status
        self.record_csv() # Auto-update CSV

    # delete task is not optimal because my main goal is to keep all records and use the csv file to analyze later with pandas. Implementing a python notebook later on.
    def delete_task(self, task_id):
        if task_id not in self.tasks:
            raise KeyError(f"Task ID {task_id} not found")
        del self.tasks[task_id] 

    def get_task(self, task_id):
        return self.tasks.get(task_id)
    


class ExecutionSimulator:
    # Milestone 5: Execution Simulation
    # I. Simulates time progression
    # II. Tracks idle time
    # III. Detects missed deadlines
    # IV. Logs execution order   
    # You are no longer choosing tasks abstractly — you are playing the schedule forward in time, like a CPU scheduler or production system.
    # Instead of adding time += 1 you jump to the next event. Event-driven simulation.
    # What this scheduler is optimal at? Your design is locally optimal at decision time. It makes the best decision right now, without knowing future arrivals or downstream effects.

    DEADLINE_TIME_MAP = {
    'INTERNAL': 5,
    'EXTERNAL': 10,
    'HARD': 7,
    'SOFT': 15
}
    
    """
    Simulates task execution over time using an event-driven model.
    Tracks:
    - execution order
    - idle time
    - missed deadlines
    """

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.current_time = 0

        self.execution_log = []      # (task_id, start, end)
        self.missed_deadlines = []   # task_id
        self.idle_time = 0

    def _deadline_time(self, task):
        """
        Converts semantic deadlines into numeric time bounds.
        """
        return task.time_line + self.DEADLINE_TIME_MAP[task.deadline]

    def run(self, task_manager):
        """
        Event-driven execution loop.
        Time advances only when an event occurs.
        """
        while True:
            task = self.scheduler.pop_next_task()

            if task is None:
                break  # No more executable tasks

            # -----------------------
            # Handle idle time
            # -----------------------
            if task.time_line > self.current_time:
                idle_gap = task.time_line - self.current_time
                self.idle_time += idle_gap
                self.current_time = task.time_line
                # Idle time represents inefficiency due to poor arrival alignment or scheduling strategy.

            # -----------------------
            # Execute task
            # -----------------------
            start_time = self.current_time
            end_time = start_time + task.duration
            self.current_time = end_time

            task.status = 'COMPLETED'

            # -----------------------
            # Log execution
            # -----------------------
            self.execution_log.append(
                (task.task_id, start_time, end_time)
            )

            # -----------------------
            # Deadline miss check
            # -----------------------
            if end_time > self._deadline_time(task):
                self.missed_deadlines.append(task.task_id)
            # detect deadline violations after execution, not during selection.”

            # -----------------------
            # Unlock dependent tasks
            # -----------------------
            if hasattr(self.scheduler, "complete_task"):
                self.scheduler.complete_task(task, task_manager)

class Scheduler:
    # Milestone 2: Priority-Based Task Scheduling
    # Always pick the best next task.
    # Priority rules (min-heap):
    # I. Priority: CRITICAL > HIGH > MEDIUM > LOW > NEGLIGIBLE
    # II. Deadline: INTERNAL > EXTERNAL > HARD > SOFT   
    # III. Timeline: FIFO (earliest created first)

    PRIORITY_ORDER = {
        'CRITICAL': 1,
        'HIGH': 2,
        'MEDIUM': 3,
        'LOW': 4,
        'NEGLIGIBLE': 5
    }

    DEADLINE_ORDER = {
        'INTERNAL': 1,
        'EXTERNAL': 2,
        'HARD': 3,
        'SOFT': 4
    }

    def __init__(self):
        self.heap = []
        

    def _task_key(self, task):
        # Generate heap comparison key.
        return (
            Scheduler.PRIORITY_ORDER[task.priority],
            Scheduler.DEADLINE_ORDER[task.deadline],
            task.time_line
        )

    def add_task(self, task):
        # The task is dependency-safe.
        # It becomes eligible for execution.
        heapq.heappush(self.heap, (self._task_key(task), task))

    def _clean_heap(self):
        # Remove tasks that were lazily deleted.

        while self.heap and self.heap[0][1].deleted:
            heapq.heappop(self.heap)

    def peek_next_task(self):
        # Look at the next task without removing it.
        self._clean_heap()
        if not self.heap:
            return None
        return self.heap[0][1]

    def pop_next_task(self):
        # Get and remove the next task to execute.
        self._clean_heap()
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[1]

    def delete_task(self, task_id):

        # Lazy deletion of a task by ID.
        # Instead of removing items from the heap: Mark task.deleted = True
        # Physically remove only when popped
        #This avoids O(n) heap rebuilds.

        for _, task in self.heap:
            if task.task_id == task_id:
                task.deleted = True
                return
        raise KeyError(f"Task ID {task_id} not found in scheduler")

    def update_priority(self, task_id, new_priority):

        # Update task priority using lazy deletion + reinsertion.

        if new_priority not in Scheduler.PRIORITY_ORDER:
            raise ValueError("Invalid priority value")

        for _, task in self.heap:
            if task.task_id == task_id:
                task.deleted = True  # mark old version
                task.priority = new_priority
                task.deleted = False
                heapq.heappush(self.heap, (self._task_key(task), task))
                return

        raise KeyError(f"Task ID {task_id} not found in scheduler")


class DependencyManager:

    # Milestone 3: Dependency Management and Cycle Detection.
    # I. Directed graph to represent dependencies.
    # II. Cycle detection using DFS with recursion stack.
    # Handles task dependencies using a directed graph.
    # The key rules, a task is schedulable only if indegree == 0,
    # Completing a task: frees dependent tasks and pushes them into heap when ready

    """
    Internal Structure:

    graph = {
            "T01FI": ["T03EN"]
        }
    indegree = {
        "T01FI": 0,
        "T03EN": 1
    }
    """
    
    def __init__(self):
        
        self.graph = defaultdict(list) # task_id -> list of task_ids that depend on it.
        self.indegree = defaultdict(int) # task_id -> number of unmet dependencies.

    def add_task(self, task_id):
        if task_id not in self.indegree:
            self.indegree[task_id] = 0


    def add_dependency(self, before_task_id, after_task_id):
        """
        If task A depends on B, then B → A
        before_task_id must be completed first and makes topological sorting natural.
        """

        self.graph[before_task_id].append(after_task_id)
        self.indegree[after_task_id] += 1

    def has_cycle_dfs(self):
        # Detect cycles using DFS with recursion stack.
        # It uses: visited and recursion stack sets.
        # Detects back edges → cycle → ❌ invalid schedule.

        visited = set() # node fully processed
        recursion_stack = set() # nodes currently in DFS path

        def dfs(node):
            """
            DFS is for validation only.
            DFS with recursion stack works because any back-edge in a directed graph indicates a cycle.
            In a directed graph:
                1. A back edge means. You are trying to visit a node that is already active in your call stack.
            This implies a cycle.
            Can DFS detect cycles in undirected graphs? No with a parent check. But in directed graph, the recursion stack is sufficient.

            # Yes, I validate dependencies using DFS with a recursion stack. If during traversal I encounter a node already in the active call stack, I detect a circular dependency.
            # This runs in O(V + E) time and works well for dependency validation before scheduling.
            # """
            visited.add(node)
            recursion_stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True

            recursion_stack.remove(node)
            return False

        for node in self.indegree:  # FIXED
            if node not in visited:
                if dfs(node):
                    return True

        return False
    
class DependencyAwareScheduler(Scheduler):

    # Uses your existing classes, but only schedules tasks whose dependencies are met.
    # Detects cycles using DFS, Executes tasks correctly. It also combines: priority scheduling and dependency resolution
    
    def __init__(self, dependency_manager):
        super().__init__()
        self.dependency = dependency_manager

    def add_task_if_ready(self, task):

        if self.dependency.indegree[task.task_id] == 0:
            super().add_task(task)

    def complete_task(self, task, task_manager):
        task.status = 'COMPLETED'

        for dependent_id in self.dependency.graph[task.task_id]:
            self.dependency.indegree[dependent_id] -= 1
            if self.dependency.indegree[dependent_id] == 0:
                dependent_task = task_manager.get_task(dependent_id)
                super().add_task(dependent_task)

"""
Task        → data + validation
TaskManager → storage + CSV
DependencyManager → dependency graph + cycle validation
Scheduler  → priority-based execution (heap)
"""

import heapq

class DFSTopologicalHeapScheduler:

    # Milestone 4 (DFS Version):
    # I. DFS + recursion stack for dependency resolution.
    # II. Heap for priority-based execution choice.
    # Priority integration using Heap and Topological Sort via DFS.

    def __init__(self, task_manager, dependency_manager):
        self.task_manager = task_manager
        self.dependency = dependency_manager
        self.visited = set()
        self.rec_stack = set()
        self.heap = []
        self.execution_order = []

    def _task_key(self, task):
        return (
            Scheduler.PRIORITY_ORDER[task.priority],
            Scheduler.DEADLINE_ORDER[task.deadline],
            task.time_line
        )

    def _dfs(self, task_id):
        """
        DFS traversal that guarantees:
        - Dependencies are resolved first
        - Cycles are detected via recursion stack
        """
        if task_id in self.rec_stack:
            raise RuntimeError("Cycle detected during DFS")

        if task_id in self.visited:
            return

        self.visited.add(task_id)
        self.rec_stack.add(task_id)

        for dependent_id in self.dependency.graph[task_id]:
            self._dfs(dependent_id)

        # Post-order position → dependencies already handled
        task = self.task_manager.get_task(task_id)
        heapq.heappush(self.heap, (self._task_key(task), task))

        self.rec_stack.remove(task_id)

    def generate_execution_order(self):
        """
        Generates a valid execution order using:
        - DFS for dependency resolution
        - Heap for priority selection
        """
        # Run DFS from all nodes (handles disconnected graphs)
        for task_id in self.dependency.indegree:
            if task_id not in self.visited:
                self._dfs(task_id)

        # Extract tasks in priority order
        while self.heap:
            _, task = heapq.heappop(self.heap)
            self.execution_order.append(task)

        return self.execution_order


manager = TaskManager()
dependency = DependencyManager()
schedule = Scheduler()
scheduler = DependencyAwareScheduler(dependency)


# Example Usage:

# 1. Create tasks
t1 = Task(priority='HIGH', deadline='HARD', duration=3, status='PENDING', department='FINANCE')
t2 = Task(priority='LOW', deadline='INTERNAL', duration=2, status='PENDING', department='HR')
t3 = Task(priority='MEDIUM', deadline='EXTERNAL', duration=4, status='PENDING', department='ENGINEERING')

# 2. Store tasks
manager.add_task(t1)
manager.add_task(t2)
manager.add_task(t3)

# 3. Register tasks in dependency graph
dependency.add_task(t1.task_id)
dependency.add_task(t2.task_id)
dependency.add_task(t3.task_id)

# 4. Add dependencies
dependency.add_dependency(t1.task_id, t3.task_id)

# 5. Validate DAG
# Cycle check (MANDATORY)
# No cycle → continue.
if dependency.has_cycle_dfs():
    raise RuntimeError("Circular dependency detected")

# 6. Initialize correct scheduler
scheduler = DependencyAwareScheduler(dependency)

# 🔑 7. INITIAL DEPENDENCY-AWARE LOAD
for task in manager.tasks.values():
    scheduler.add_task_if_ready(task)

# 8. Normal execution
next_task = scheduler.pop_next_task()
scheduler.complete_task(next_task, manager)

print(scheduler.peek_next_task())
