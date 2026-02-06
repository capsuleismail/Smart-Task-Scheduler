import random

# Ensure reproducibility
random.seed(22)

tasks = 1000

def generate_tasks(num_tasks = task):
    """
    Generate a list of task dictionaries with randomized attributes.
    """

    priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NEGLIGIBLE']
    deadlines = ['INTERNAL', 'EXTERNAL', 'HARD', 'SOFT']
    durations = ['1', '2', '3', '4', '5']
    status = ['PENDING', 'ONGOING', 'COMPLETED']
    departments = [
        'HR', 'ENGINEERING', 'MARKETING',
        'SALES', 'FINANCE', 'IT', 'CUSTOMER_SUPPORT'
    ]

    return [
        [random.choice(priorities),
           random.choice(deadlines),
            random.choice(durations),
           random.choice(status),
            random.choice(departments),
        ]
        for _ in range(num_tasks)
    ]


if __name__ == "__main__":
    tasks = generate_tasks(tasks)
    print(tasks)
    print(f"Generated {len(tasks)} tasks.")
