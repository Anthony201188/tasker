import algo_utils as algo
import class_def

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
    class_def.Task("Task 17", "Description 17", 7, 5, "Category 11", "17-08-23"),
    class_def.Task("Task 18", "Description 18", 8, 4, "Category 12", "18-08-23"),
    class_def.Task("Task 19", "Description 19", 5, 3, "Category 2", "19-08-23"),
    class_def.Task("Task 20", "Description 20", 6, 2, "Category 13", "20-08-23"),
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
        algo.pre_sort(item, focus1, focus2)
    
    
    fully_sorted = algo.task_sort(class_def.task_tracking.non_urgent_task_stack.stack, focus1, focus2)

    print("fully sorted",fully_sorted)

    # set the stack to the fully_sorted order
    class_def.task_tracking.non_urgent_task_stack.stack = fully_sorted
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
    


