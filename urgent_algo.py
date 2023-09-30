from class_def import task_tracking   # import specifics to reduce circular dependencies

##### define the urgent sorting method #####

# sorting for urgent stack
def urgent_custom_sort_key(task):
    # Return a tuple for sorting key
    return ( task.due_date , int(task.urgency ,int(task.importance)))  


def sort_urgent_tasks()->None:
    urgent_tasks_sorted = sorted(task_tracking.urgent_stack, key=urgent_custom_sort_key)
    task_tracking.urgent_stack = urgent_tasks_sorted
    task_tracking.urgent_stack.print_task_stack()



    