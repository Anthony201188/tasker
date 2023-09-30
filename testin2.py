""" import pickle
import os
daily_task_entry_lst = [
{"entry_name":"entry","content":"test123" ,"load_on_start":True},
{"entry_name":"entry2","content":"test345" ,"load_on_start":True},
{"entry_name":"entry3","content":"test789" ,"load_on_start":False},
]

with open("daily_task_entry_lst.pkl", "wb") as file:
    pickle.dump(daily_task_entry_lst, file)

 """


# def load_required_file(file_path):
#     """ checks whether the file needs to be loaded or not, returns the contents of the bin file as a python var """
#     with open(file_path, 'rb') as file:
#         data = pickle.load(file)
#         if data.get("load_on_start", False): #<-second param here is default val
#                 return data
#         else:
#             print(f"File [{file_path}] not required to be loaded")


# # Example usage
# contents = load_required_file("daily_task_entry.pkl")
# print(contents) 

# import os
# current_directory = os.getcwd()
# daily_task_files = [os.path.join(root, file) for root, _, files in os.walk(current_directory) for file in files if "daily_task" in file]

# print(daily_task_files)

# if daily_task_files:
#     print("Daily task files found:")
#     for file in daily_task_files:
#         print(file)
# else:
#     print("No daily task files found in the current directory and its subdirectories.")


''' class Stack:
    """Used to store/manage tasks, will need some kind of file persistence implemented."""
    def __init__(self):
        self.stack = []

    def add_task(self, task, position=None):
        """
        Adds task obj to stack(obj) by task name attribute (str).
        Can take an optional third argument to add it at a certain position.
        """
        if position is not None:
            self.stack.insert(position, task)
        else:
            self.stack.append(task)

    def remove_task(self, task_name):
        """
        Removes task obj from stack(lst) by task name attribute (str).
        """
        self.stack = [task for task in self.stack if task.name != task_name]

    def print_task_stack(self):
        for task in self.stack:
            print(task.name)


class TaskTracking:
    id_counter = 0
    task_list = []


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


# Creating instances of the Task class
task1 = Task("Task 1", "Description 1", 2, 3, "Category A", "2023-08-31")
task2 = Task("Task 2", "Description 2", 1, 2, "Category B", "2023-09-15")
task3 = Task("Task 3", "Description 3", 3, 1, "Category A", "2023-09-01")

# Creating an instance of the Stack class
task_stack = Stack()

# Adding tasks to the stack
task_stack.add_task(task1)
task_stack.add_task(task2)
task_stack.add_task(task3)

# Removing a task by name
task_stack.remove_task("Task 2")

# Printing the updated stack
task_stack.print_task_stack() '''


""" from app import save_file
from class_def import task_tracking


# testing the task_tracking instance created in class_def 
#NOTE -  this is how it should it should function when its in the app.py script
#NOTE - its worth creating good concicie doc strings so that I can see whats needed type and arg wise.

task_tracking.create_task("washing", "do the washing", 8, 4, "household","20-11-88")
task_tracking.create_task("cleaning", "clean the house", 6, 2, "household","20-11-88")

print(task_tracking.all_tasks)
display  = task_tracking.get_display_task()
print(display)
washing = task_tracking.get_task("washing")
task_tracking.set_display_task(washing)
print(task_tracking.get_display_task())

save_file("task_tracking.pkl",task_tracking) """


#save_file("task_tracking.pkl", task_tracking)

##### factory method example #####

""" import tkinter as tk

class Product:
    def __init__(self, name):
        self.name = name

class ProductFactory:
    @staticmethod
    def create_product(product_type, name):
        if product_type == "A":
            return ProductA(name)
        elif product_type == "B":
            return ProductB(name)
        else:
            raise ValueError("Invalid product type")

class ProductA(Product):
    pass

class ProductB(Product):
    pass

def create_product():
    product_type = product_type_var.get()
    name = name_entry.get()

    new_product = ProductFactory.create_product(product_type, name)

    # Display new_product details in GUI

# GUI setup
root = tk.Tk()

product_type_var = tk.StringVar()
name_entry = tk.Entry(root)
create_button = tk.Button(root, text="Create Product", command=create_product)

# Arrange GUI elements and start the main event loop
# ...

root.mainloop() """

""" import customtkinter 
def switch_event():
    print("switch toggled, current value:", switch_var.get())

switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(root, text="CTkSwitch", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")

root.mainloop() """
from datetime import datetime
def within_7_days_or_past(date_str):
    try:
        # Parse the input date string into a datetime object
        input_date = datetime.strptime(date_str, '%d-%m-%y')
        
        # Get the current date
        current_date = datetime.now()
        
        # Calculate the timedelta between the input date and the current date
        time_delta = input_date - current_date

        # Check if the timedelta is within the next 7 days or past todays date
        return (time_delta.days <= 0 and time_delta.days <= 7) or (current_date.date() == input_date.date()) #effectivley a compound condition that will only return true ig both condtions are met at the same time
   
    except ValueError as e:
        # If there's an error in parsing the string
        print(f"Error:{type(e).__name__} - {e}")
        return False

print(within_7_days_or_past('30-09-23')) #true
print(within_7_days_or_past('09-10-23')) #false
print(within_7_days_or_past('21-09-23')) #true