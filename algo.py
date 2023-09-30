# write the algo sorting method for tasks here 
#### utils
import class_def
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

#### testing
# print(within_7_days_or_past('30-09-23')) #true
# print(within_7_days_or_past('09-10-23')) #false
# print(within_7_days_or_past('21-09-23')) #true
####


#### main pre-sort decision making #### 

##  TODO -  will need to define sorting fucntions for both project and urgent lists could use the sorting method here adapted

##### PRE-SORT UTILS #####
#need to change this function to account for overdue items to return true as well
def is_urgent(task_class_obj)->bool:
    """ takes a instance_of_task_object as an argument and returns <type=bool> if the .due_date attribute is within the next 7 days is true  """
    date_str = task_class_obj.due_date #<- type = string
    print("task date",date_str,type(date_str))
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

def pre_sort(task_class_obj, *foci)->None:
    """ 
    Takes a Task class obj as an argument, monthly focus1/2 and pre-sorts the task according to "not a blank diagram.jpg"
    will sort tasks into the following:
    -archive task (add to archive and remove from main task list)
    -urgent
    -non-urgent (bottom of stack)
    returns: None
    """
# TODO - add some kind of overdue date handling here as well 
#otherwise things not in the enxt 7 days become non urgent again!

    if task_class_obj.done:
        #Add task to archive whilst removing from task_tracking.all_tasks
        class_def.task_tracking.task_archive.add_task_from_main(task_class_obj)
        print(f"{task_class_obj} added to TaskArchive.task_archive")

    else:
        # Sends objects to urgent stack if due in next 7 days
        if is_urgent(task_class_obj):
            class_def.task_tracking.urgent_stack.add_task_from_main(task_class_obj)#add to urgent stack whilst removing from all_tasks
            print(f"{task_class_obj} added to task_tacking.urgent_stack")

        else:
            # Sorting Remaining, non-urgent priority stack

            #In monthly focus1/2 then top of the list
            if task_cat_in_month_foci(task_class_obj, *foci):
                class_def.task_tracking.non_urgent_task_stack.add_task_from_main(task_class_obj,0)
                print(f"{task_class_obj} added to task_tacking.non_urgent_stack, tracing:algo_utils:if")

            
            #Else bottom of the list
            else:
                class_def.task_tracking.non_urgent_task_stack.add_task_from_main(task_class_obj)
                print(f"{task_class_obj} added to task_tacking.non_urgent_stack (-1), tracing:algo_utils:else")

# TODO - sorting seems to work ok, need to work on the print overiding and the other print statments
# need to find a way to seach all classes for a tasks to monitor them across multiple stacks.
# implement a TasjTracking method called "find", which searches all class attributes and returns any locations of task by id
# implement a TasjTracking method called "show all", which searches all class attributes and returns a list of name attributes in each stack






# Task sorting 

# split the stack on monthly focus
def split_focus_stack(task_list, focus1, focus2)->list:
    # NOTE - needs error handling should somehow tasks that are niether in focus1 or focus2 or fuzzy matching, might need to add some kind of 
    #constraints on entering the catagories to standardise the format to reduce mismatching errors.
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
        if task.category == focus1:#<- here is where I would put the fuzzy matching
            matching_focus1.append(task)
        elif task.category == focus2:
            matching_focus2.append(task)

    return matching_focus1, matching_focus2

#commented out as I think the use of sets was introducing some inconcsitant random ordering but good function for comparing and combining
""" def compare_combine(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    # Elements that are in both lists
    common_elements = list(set1 & set2)

    # Elements that are unique to each list
    unique_to_list1 = list(set1 - set2)
    unique_to_list2 = list(set2 - set1)

    #combine
    combined = common_elements + unique_to_list1

    return combined """

def compare_combine(list1, list2):
    """ compare the lists and add the unique elements from list2 to that of the existing elements of list1 """
    temp_data = [] 

    for item in list1:
        if item not in list2:
            temp_data.append(item)

    combined = list2 + temp_data

    return combined

            

# TODO needs testing and some sort of task manament at the end to update the nonurgent task list aybe a class method


    



            
def shuffle_with_ratio(list1, list2):
    #TODO - although this shuffle works it takes the already sorted by importance 
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


# sorting
def custom_sort_key(task):
    # Return a tuple of ( importance, urgency,due_date,) for sorting - passes each task in the list to get the attributes and then sorts accordingly
    return ( int(task.importance), int(task.urgency)) # TODO = ,task.due_date should be implemented but globally the data format needs to be changed to yy-mm-dd so that it can be numerially accuratley sorted


## full task sorting algo
def task_sort(task_list, focus1, focus2):
    #TODO - look at this function, changing the custom sort key or the second shuffle makes no difference to the orders....
    """ takes a list of task objects and the monthly focus1/2 as args. splits that list into two based on foci then sorts based on custom sorting key finally shuffling together using a 3:1 ration """
    print("task sort called ()")
    print(f"task list in full pre-sort", [item.name for item in task_list])
    # split the list
    tuple_of_lists = split_focus_stack(task_list, focus1, focus2)
 
    list1, list2 = tuple_of_lists # unpack the tuple
    print("split focus1 list:",[item.name for item in list1 ])
    print("split focus2 list:",[item.name for item in list2 ])
    

    # sort the lists
    # TODO - dont know if this sort is needed test the order without this using the (2nd) sort after shuffle it shouldnt make any difference.
    sorted_list1 = sorted(list1, key=custom_sort_key)
    print("sorted list1 :",[item.name for item in sorted_list1 ])
    sorted_list2 = sorted(list2, key=custom_sort_key)
    print("sorted list2 :", [item.name for item in sorted_list2])

    #shuffles the lists 3:1
    shuffled_list = shuffle_with_ratio(sorted_list1, sorted_list2)
    #combined_shuffled_sorted = list1 + list2
    print("shuffled_list", [item.name for item in shuffled_list]) #< NOTE - i think this isnt shuffling them as there is only 6 and it shuffles 3:1 try 2:1 or add more cat1/2 tasks

    #sor againa fter the shuffle
    sorted_and_shuffled = sorted(shuffled_list, key=custom_sort_key, reverse=True) 
    print("sorted and shuffled list (2nd sort)", [item.name for item in sorted_and_shuffled])


    #compare the lists and add back in the original tasks
    combined_shuffled_sorted = compare_combine( task_list, sorted_and_shuffled) #START FROM HERE  need to get the correct order from the above list to copy correcectly to the front of this list
    print("combined and shuffled list (final)", [item.name for item in combined_shuffled_sorted])

    

    return combined_shuffled_sorted
            














############### test-cases ##
#from class_def import Task

""" # instantiate Task objects
washing = class_def.Task("washing", "do the washing", 8, 4, "household","03-08-23")
cleaning = class_def.Task("cleaning", "clean the house", 6, 2, "household","20-21-88")
foci =("household", "maths")
 

# Testing the catagory month focus matching
print(task_cat_in_month_foci(washing,foci,"household"))#<-should return True, PASS
print(task_cat_in_month_foci(washing,"science","music"))#<-should return False, PASS

print(washing.due_date)
print(is_urgent(washing))

#pre-sorting checks
pre_sort(washing) """
print("test")

""" # Testing Task class list, counter and instance id
print(Task.task_list, Task.id_counter, washing.id_,cleaning.id_ )#<- should return list of all instaces, total num of instance, unique id of insace 3 and 4, PASSED
##
print(due_date_within_next_week(washing)) #<- should return "Is within next 7 days:" True, PASSED

print(due_date_within_next_week(cleaning)) #<- should return "Is within next 7 days:" False,  PASSED """

## sort testing
""" # Sample data with instances of the Task class
data = [
    class_def.Task("Task 1", "Description 1", 8, 4, "Category 1", "03-08-23"),
    class_def.Task("Task 2", "Description 2", 5, 2, "Category 2", "02-08-23"),
    class_def.Task("Task 3", "Description 3", 6, 3, "Category 1", "01-08-23"),
]

# Sort the data using the custom_sort_key
sorted_data = sorted(data, key=custom_sort_key)

# Print the sorted data
for task in sorted_data:
    print(f"{task.name} - Importance: {task.importance} - Urgency: {task.urgency} - Due Date: {task.due_date} ") """

#############################
def main():
    #create mock main task list
    test_data = [
        class_def.Task("Task 1", "Description 1", 8, 4, "Category 1", "03-08-23",done=True), #add this to check filtering ->,done=True
        class_def.Task("Task 2", "Description 2", 5, 2, "Category 2", "25-09-23"), # this one is now urgent
        class_def.Task("Task 3", "Description 3", 6, 3, "Category 1", "01-08-23"),
        class_def.Task("Task 4", "Description 4", 7, 5, "Category 3", "04-08-23"),
        class_def.Task("Task 5", "Description 5", 9, 2, "Category 2", "05-08-23"),
        class_def.Task("Task 6", "Description 6", 4, 1, "Category 4", "06-08-23"),
        class_def.Task("Task 7", "Description 7", 5, 3, "Category 5", "07-08-23"),
        class_def.Task("Task 8", "Description 8", 7, 4, "Category 1", "08-08-23"),
        class_def.Task("Task 9", "Description 9", 6, 2, "Category 6", "09-08-23"),
        class_def.Task("Task 10", "Description 10", 8, 5, "Category 7", "10-08-23"),
        class_def.Task("Task 11", "Description 11", 5, 3, "Category 2", "11-08-23"),
        class_def.Task("Task 12", "Description 12", 6, 1, "Category 8", "12-08-23"),
        class_def.Task("Task 13", "Description 13", 7, 4, "Category 9", "13-08-23"),
        class_def.Task("Task 14", "Description 14", 4, 2, "Category 3", "14-08-23"),
        class_def.Task("Task 15", "Description 15", 5, 3, "Category 10", "15-08-23"),
        class_def.Task("Task 16", "Description 16", 6, 2, "Category 1", "16-08-23"),
        class_def.Task("Task 17", "Description 17", 7, 5, "Category 11", "10-10-23"),
        class_def.Task("Task 18", "Description 18", 8, 4, "Category 12", "10-10-23"),
        class_def.Task("Task 19", "Description 19", 5, 3, "Category 2", "10-10-23"),
        class_def.Task("Task 20", "Description 20", 6, 2, "Category 13", "10-10-23"),
    ]

    focus1 = "Category 1"
    focus2 = "Category 2"


    #check the objects have been created
    print("obj check",test_data[1])

    #pre sorting check whats in each stack
    print("PRE-SORTING TESTING")
    print()
    print("'pre-sort'class_def.all_tasks",class_def.task_tracking.string_list_all_tasks())
    print("'pre-sort'class_def.task_archive",class_def.task_tracking.task_archive.return_stack_names())
    print("'pre-sort'class_def.urgent_task_stack",class_def.task_tracking.non_urgent_task_stack.return_stack_names())
    print("'pre-sort'class_def.non_urgent_task_stack",class_def.task_tracking.non_urgent_task_stack.return_stack_names())
    print("'pre-sort'class_def.project_task_stack",class_def.task_tracking.project_stack.return_stack_names())

    def full_sort(task_obj_list, focus1, focus2):
        
        for item in task_obj_list:
            pre_sort(item, focus1, focus2) # pre-sort its missing task3 for some reason even though its "catagory 1"
        
        
        fully_sorted = task_sort(class_def.task_tracking.non_urgent_task_stack.stack, focus1, focus2)


        # set the stack to the fully_sorted order
        class_def.task_tracking.non_urgent_task_stack.stack = fully_sorted # the fully sorted list is then dropping all tasks not in cat1 or 2 this shouldnt happen look at split_focus_stack function
        print("Tasks successfully sorted")
        return fully_sorted

    #run the function
    list1 = full_sort(test_data, focus1, focus2)

    #post-sort testing
    print("POST-SORTING TESTING")
    print()
    print("'post-sort'class_def.all_tasks",class_def.task_tracking.string_list_all_tasks())
    print("'post-sort'class_def.task_archive",class_def.task_tracking.task_archive.return_stack_names())
    print("'post-sort'class_def.urgent_task_stack",class_def.task_tracking.urgent_stack.return_stack_names())
    print("'post-sort'class_def.non_urgent_task_stack",class_def.task_tracking.non_urgent_task_stack.return_stack_names())
    print("'post-sort'class_def.project_task_stack",class_def.task_tracking.project_stack.return_stack_names())


        


