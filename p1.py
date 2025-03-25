from datetime import datetime, timedelta
import operator

# Task class to store task details
class Task:
    def __init__(self, name, deadline, est_time, priority):
        self.name = name
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")  # e.g., "2025-03-30 17:00"
        self.est_time = float(est_time)  # Estimated time in hours
        self.priority = int(priority)  # 1 (low) to 5 (high)

    def __str__(self):
        return f"{self.name} (Due: {self.deadline}, Time: {self.est_time}h, Priority: {self.priority})"

# Function to calculate urgency score based on deadline
def calculate_urgency(task, current_time):
    time_left = (task.deadline - current_time).total_seconds() / 3600  # Hours until deadline
    if time_left <= 0:
        return 100  # Max urgency if overdue
    return max(10, 100 / time_left)  # Inverse proportionality, min score 10

# Function to prioritize tasks
def prioritize_tasks(tasks, current_time):
    task_scores = {}
    for task in tasks:
        urgency = calculate_urgency(task, current_time)
        score = (urgency * 0.6) + (task.priority * 10 * 0.4)  # Weighted: 60% urgency, 40% priority
        task_scores[task] = score
    # Sort tasks by score (highest first)
    sorted_tasks = sorted(task_scores.items(), key=operator.itemgetter(1), reverse=True)
    return [task for task, score in sorted_tasks]

# Function to suggest a schedule based on user preference
def suggest_schedule(tasks, work_start, work_end, morning_person):
    current_time = datetime.now()
    schedule = []
    available_time = work_start

    for task in tasks:
        # Adjust task placement based on morning_person preference
        if morning_person and available_time.hour > 12:  # After noon, shift to next morning
            available_time = work_start + timedelta(days=1)
        elif not morning_person and available_time.hour < 12:  # Before noon, shift to evening
            available_time = work_end - timedelta(hours=task.est_time)

        # Check if task fits in available time
        task_end = available_time + timedelta(hours=task.est_time)
        if task_end > work_end:
            print(f"Warning: '{task.name}' doesn't fit today. Moving to next day.")
            available_time = work_start + timedelta(days=1)
            task_end = available_time + timedelta(hours=task.est_time)

        # Add to schedule if not overdue
        if task_end <= task.deadline:
            schedule.append((task, available_time, task_end))
            available_time = task_end
        else:
            print(f"Warning: '{task.name}' cannot be scheduled before deadline.")

    return schedule

# Main function to run the program
def main():
    print("Welcome to the AI Time Management Coach!")
    tasks = []

    # User preference input
    morning_person = input("Are you a morning person? (yes/no): ").lower() == "yes"
    work_start = datetime.strptime(input("Enter work start time (e.g., 2025-03-25 09:00): "), "%Y-%m-%d %H:%M")
    work_end = datetime.strptime(input("Enter work end time (e.g., 2025-03-25 17:00): "), "%Y-%m-%d %H:%M")

    # Task input loop
    while True:
        add_task = input("Add a task? (yes/no): ").lower()
        if add_task != "yes":
            break
        name = input("Task name: ")
        deadline = input("Deadline (e.g., 2025-03-30 17:00): ")
        est_time = input("Estimated time (hours, e.g., 2.5): ")
        priority = input("Priority (1-5, 5 being highest): ")
        tasks.append(Task(name, deadline, est_time, priority))

    if not tasks:
        print("No tasks to prioritize.")
        return

    # Prioritize and schedule
    current_time = datetime.now()
    prioritized_tasks = prioritize_tasks(tasks, current_time)
    schedule = suggest_schedule(prioritized_tasks, work_start, work_end, morning_person)

    # Display results
    print("\nPrioritized Tasks:")
    for i, task in enumerate(prioritized_tasks, 1):
        print(f"{i}. {task}")

    print("\nSuggested Schedule:")
    for task, start, end in schedule:
        print(f"{task.name}: {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()