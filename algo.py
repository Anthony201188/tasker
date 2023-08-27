# write the algo sorting method for tasks here as a class . use eisenhower and any other prioitisation methods you so wish
# write the algo sorting method for tasks here 
#### utils
from datetime import datetime, timedelta
from class_def import *
def within_7_days_or_past(date_str):
    try:
        # Parse the input date string into a datetime object
        input_date = datetime.strptime(date_str, '%d-%m-%y')

        # Get the current date
        current_date = datetime.now()

        # Calculate the timedelta between the input date and the current date
        time_delta = input_date - current_date

        # Check if the timedelta is within the next 7 days or past todays date
        return (0 <= time_delta.days <= 7) or (current_date.date() == input_date.date()) #effectivley a compound condition that will only return true ig both condtions are met at the same time

    except ValueError as e:
        # If there's an error in parsing the string, handle it gracefully
        print(f"Error: {e}")
        return False

#### Example usage:
# date_str = "20-11-88"  # Replace this with your desired date string
# is_within_7_days = is_within_next_seven_days(date_str)
# print("Is within next 7 days:", is_within_7_days)
####


#### main pre-sort decision making 
def check_task_status_done(task_class_obj):
    """Check the status of the "task_class_object" and return True if it's done, otherwise return False."""
    return task_class_obj.done


#need to change this function to account for overdue items to return true as well
def is_urgent(task_class_obj)->bool:
    """ takes a instance_of_task_object as an argument and returns <type=bool> if the .due_date attribute is within the next 7 days is true  """
    date_str = task_class_obj.due_date #<- type = string
    print(type(date_str))
    #print("Is within next 7 days:") #<- testing
    return within_7_days_or_past(date_str) # converts string to time delta and checks within the next 7 days, returns a bool

def task_cat_in_month_foci(task_class_obj, *foci) -> bool:
    """Takes a task instance and multiple monthly foci as args and returns a bool depending on if the task attribute "category" matches any of the provided foci."""
    return any(focus == task_class_obj.category for focus in foci)

#####

#pre-sort full algo
#TODO - only works if tasks start from main task list
#TODO - Some kind of task tracking across classes
#TODO - print statments to check if obj in list before printing, no blind printing

def pre_sort(task_class_obj, *foci):
    """ 
    Takes a Task class obj as an argument, monthly focus1/2 and pre-sorts the task according to "not a blank diagram.jpg"
    will sort tasks into the following:
    -TaskArchive.task_archive
    -TaskNonurgent.non_urgent_stack/bottom[0]
    -TaskNonurgent.non_urgent_stack/bottom[-1]
    -Urgent
    """

    if check_task_status_done(task_class_obj):
        #add task to archive
        TaskArchive.task_archive.append(task_class_obj)
        print(f"{task_class_obj} added to TaskArchive.task_archive")

        if task_class_obj in TaskArchive.task_archive:

            #remove task from main task list
            TaskTracking.task_list.remove(task_class_obj)
            print(f"{task_class_obj} removed from TaskTracking.task_list")

    else:
        # Sends objects to urgent stack if due in next 7 days
        if is_urgent(task_class_obj): # confusing of two within 7 days functions change!
            TaskTracking.task_list.remove(task_class_obj)
            print(f"{task_class_obj} \n Was successfully removed from the TaskTracking.task_list")
            TaskUrgent.urgent_stack.append(task_class_obj)
            print(f"{task_class_obj} \n Was successfully added to the TaskUrgent.urgent_stack")

        else:
            # Remaining, Non-Urgent priority stack sorted

            #In monthly focus1/2 then top of the list
            if task_cat_in_month_foci(task_class_obj, *foci):
                TaskTracking.task_list.remove(task_class_obj)
                print(f"{task_class_obj} \n Was successfully removed frin the TaskTracking.task_list")
                TaskNonUrgent.non_urgent_stack.insert(-1, task_class_obj)
                print(f"{task_class_obj} \n successfully added to TaskNonUrgent.non_urgent_stack, pos -1")

            #Else bottom of the list
            else:
                TaskTracking.task_list.remove(task_class_obj)
                print(f"{task_class_obj} was successfully removed frin the TaskTracking.task_list")
                TaskNonUrgent.non_urgent_stack.insert(0, task_class_obj)
                print(f"{task_class_obj} successfully added to TaskNonUrgent.non_urgent_stack, pos 0")

# TODO - sorting seems to work ok, need to work on the print overiding and the other print statments
# need to find a way to seach all classes for a tasks to monitor them across multiple stacks.
# implement a TasjTracking method called "find", which searches all class attributes and returns any locations of task by id
# implement a TasjTracking method called "show all", which searches all class attributes and returns a list of name attributes in each stack






# Task sorting 

# split the stack on monthly focus
def split_focus_stack(task_list, focus1, focus2):
    """Takes a list of task objects and splits it into two lists based on whether "focus1" or "focus2" matches their category attribute.
    Args:
        task_list (list): A list of task objects.
        focus1 (str): The first string to match against the category attribute.
        focus2 (str): The second string to match against the category attribute.
    Returns:
        tuple: A tuple containing two lists: one with task objects matching "focus1" and another with task objects matching "focus2".
    """
    matching_focus1 = []
    matching_focus2 = []

    for task in task_list:
        if task.category == focus1:
            matching_focus1.append(task)
        elif task.category == focus2:
            matching_focus2.append(task)

    return matching_focus1, matching_focus2


# sorting
def custom_sort_key(task):
    # Return a tuple of ( importance, urgency,due_date,) for sorting
    return ( task.importance, task.urgency,task.due_date)

# Sample data with instances of the Task class
data = [
    Task("Task 1", "Description 1", 8, 4, "Category 1", "03-08-23"),
    Task("Task 2", "Description 2", 5, 2, "Category 2", "02-08-23"),
    Task("Task 3", "Description 3", 6, 3, "Category 1", "01-08-23"),
]

# Sort the data using the custom_sort_key
sorted_data = sorted(data, key=custom_sort_key)

# Print the sorted data
for task in sorted_data:
    print(f"{task.name} - Importance: {task.importance} - Urgency: {task.urgency} - Due Date: {task.due_date} ")

def shuffle_with_ratio(list1, list2):
    """Shuffles two lists together using a ratio of 3:1.
    Args:
    list1 (list): The first list of task objects.
    list2 (list): The second list of task objects.
    Returns:
    list: The shuffled list containing task objects from both lists in a 3:1 ratio.
    """
    shuffled_list = []

    # Calculate the number of elements to take from list1 (3/4 of total elements)
    take_from_list1 = len(list1) // 4 * 3

    while len(list1) > 0 and len(list2) > 0:
        # Take 3 elements from list1
        for _ in range(min(take_from_list1, len(list1))):
            shuffled_list.append(list1.pop(0))

        # Take 1 element from list2
        shuffled_list.append(list2.pop(0))

    # Add any remaining elements from list1 (if any)
    shuffled_list.extend(list1)

    # Add any remaining elements from list2 (if any)
    shuffled_list.extend(list2)

    return shuffled_list          




# TODO needs testing and some sort of task manament at the end to update the nonurgent task list aybe a class method

## full task sorting algo
def task_sort(task_list, focus1, focus2):
    """ takes a list of task objects and the monthly focus1/2 as args. splits that list into two based on foci then sorts based on custom sorting key finally shuffling together using a 3:1 ration """

    # split the list
    tuple_of_lists = split_focus_stack(task_list, focus1, focus2)
    list1, list2 = tuple_of_lists # unpack the tuple

    # sort the lists
    sorted_list1 = sorted(list1, key=custom_sort_key)
    sorted_list2 = sorted(list2, key=custom_sort_key)

    #shuffles the lists 3:1
    shuffled_list = shuffle_with_ratio(sorted_list1, sorted_list2)

    return shuffled_list















############### test-cases ##
#from class_def import Task

# instantiate Task objects
washing = Task("washing", "do the washing", 8, 4, "household","03-08-23")
cleaning = Task("cleaning", "clean the house", 6, 2, "household","20-21-88")
foci =("household", "maths")


# Testing the catagory month focus matching
print(task_cat_in_month_foci(washing,foci,"maths"))#<-should return True, PASS
print(task_cat_in_month_foci(washing,"science","music"))#<-should return False, PASS

print(washing.due_date)
print(is_urgent(washing))

#pre-sorting checks
pre_sort(washing)

""" # Testing Task class list, counter and instance id
print(Task.task_list, Task.id_counter, washing.id_,cleaning.id_ )#<- should return list of all instaces, total num of instance, unique id of insace 3 and 4, PASSED
##
print(due_date_within_next_week(washing)) #<- should return "Is within next 7 days:" True, PASSED
print(due_date_within_next_week(cleaning)) #<- should return "Is within next 7 days:" False,  PASSED """

#############################