#refactoring of "class_def" to decouple and reduce.
#NOTE THIS VERSIONS TRACKING DOESNT WORK WELL DUE TO HAVING TO USE METHODS AND NOT CREATE NEW TASK INSTACES TO CREATE TASKS 
class Task:
    def __init__(self, name, description, urgency, importance, category, due_date, project=False, done=False):
        self.name = name
        self.description = description
        self.urgency = urgency
        self.importance = importance
        self.category = category
        self.due_date = due_date
        self.project = project
        self.done = done
        self.id_ = None  # The id_ will be assigned by the TaskTracking


    def __str__(self) -> str:
        return (f"""

                Task name: [{self.name}]
                Task description: [{self.description}]
                Task urgency:[{self.urgency}]
                Task importance:[{self.importance}]
                Task catagory:[{self.category}]
                Task due date:[{self.due_date}]
                Task status:Done=[{self.done}]
                Task id_:[{self.id_}]
                """)

class TaskTracking:
    def __init__(self):
        self.task_list = []
        self.id_counter = 0

    def add_task(self, task):
        self.task_list.append(task)
        self.id_counter += 1
        task.id_ = self.id_counter

    def remove_task(self, task):
        self.task_list.remove(task)
        self.update_ids()

    def update_ids(self):
        for index, task in enumerate(self.task_list):
            task.id_ = index + 1

class TaskDisplay:
    def __init__(self):
        self.display_task = None

    def set_display_task(self, task_id):
        for task in task_tracking.task_list:
            if task.id_ == task_id:
                self.display_task = task
                break

    def get_display_task(self):
        return self.display_task

# Example usage:
task_tracking = TaskTracking()
task_display = TaskDisplay()

task1 = Task("Task 1", "Description 1", 1, 3, "Work", "2023-08-10")
task2 = Task("Task 2", "Description 2", 2, 2, "Personal", "2023-08-15")

task_tracking.add_task(task1)
task_tracking.add_task(task2)

print(task1.id_)  # Output: 1
print(task2.id_)  # Output: 2

task_display.set_display_task(1)
display_task = task_display.get_display_task()
print(display_task.name)  # Output: "Task 1"
