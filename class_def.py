from app import load_file, save_file

class Task:

    def __init__(self,name ,description,urgency,importance,category,due_date, project=False, done=False ):
        
        #id tracking implimented to match class attribute count and index position in task_list
        TaskTracking.id_counter += 1      
        self.id_ = TaskTracking.id_counter      
        TaskTracking.task_list.append(self) 
        
        self.name = name
        self. description = description
        self.urgency = urgency
        self.importance = importance
        self.category = category
        self.due_date = due_date
        self.project = project
        self.done = done 

    def __str__(self) -> str:
        return (f"""
                Task name: [{self.name}]
                Task description: [{self.description}]
                Task urgency:[{self.urgency}]
                Task importance:[{self.importance}]
                Task catagory:[{self.category}]
                Task due date:[{self.due_date}]
                Task status:Done=[{self.done}]
                Task is a project:[{self.project}]
                Task id_:[{self.id_}]
                """)

class Project(Task):
    """ this class is used only if the task is a project it inherits from the project class but allows the adding of sub tasks within that project task """
    # write the class for project here.
    pass

class TaskTracking:
    # TODO -  needs to be a constructor so I can save the class instance on load on start for file persistance of task tracking!
    task_list = []  # contains a list of all tasks <- will neet to be changed to instance attribute
    id_counter = 0  # counts all instances of Task class
    display_task = ""

    #used to set the displayed tasks
    @classmethod    
    def set_display_task(cls, task_obj):
        cls.display_task = task_obj

    @classmethod
    def get_display_task(cls):
        return cls.display_task

    @classmethod                      
    def remove_task(cls, task):
        cls.task_list.remove(task)
        cls.update_ids()

    @classmethod
    def update_ids(cls):
        for index, task in enumerate(cls.task_list):
            task.id_ = index

      

""" Explaination ofthe id function;
-Every time a new instance is created the "self.id_" instance attribute is created and set to it's index position within the "task_list" class attribute.
-The "update_ids" class method resets all of the instances id attributes to their index position within the class attribute "task_list".
-The "remove_task" class method should be used to remove tasks from the task list as it removes the task insatance from the task_list and then calls the reset method
to reset all of the ids

**Note:
-This feature allows for a dynamic unique id  to be set for each instance of a task that matches its index number in the task.
-The class attribute "Task.id_counter" keeps track of the number of instances that have been created starting at -1 to account for the first instance.
-This allows the calling of the tasks id using list indexing elsewhere in the app.py main script.
-The id counter starts at -1 to indicate and empty list and so the id matches with the list index
## check line 168 in app.py for an example
  """

# NOTE - worth noting hrer you can paickle an instance of a class this maybe the way to store the stacks and also the main task list

############  STACK CLASSES USED FOR SORTING AND STORING TASK OBJECTS ############
class Stack:
    """ used to store/manage tasks, will need some kind of file persistance implemented.""" 
    def __init__(self):

        self.stack = []

    def add_task(self, task):
        """ adds task obj to the stack(lst) by task name attribute(str) """
        self.stack.append(task)

    def remove_task(self, task):
        """ removes task obj from stack(lst) by task name attribute (str) """
    def print_task_stack(self):
        print(self.stack)

        return self.completed_tasks

#NOTE - following three classes could be made into one class later depending on required methods and attributes
# Just use instances of same class used for stacking tasks or inheritance


class TaskArchive:
    """ used to manage completed tasks, will need some kind of file persistance implemented """
    task_archive_stack = []

class TaskNonUrgent:
    """ Used to manage all non-urgent,high-priorty tasks """
    non_urgent_stack = [] # could use dequws for these

class TaskUrgent:
    """ Used to manage all urgent tasks """
    urgent_stack = []




# TODO - implement some kind of log, that logs everything printed to the terminal every "session" (nice to have)



""" class DaysProgress:

    history = [list_of_instances, inst2]

    def __init__(self, datestamp , JSON):
    
        #datestamp = timenow.localtime()

        # use JSON or nested dict for this
        self.checkbox1 = {"datestamp": "done=bool"}
        self.checkbox2 = {"datestamp": "done=bool"}
        self.checkbox3 = {"datestamp": "done=bool"}
        self.checkbox4 = {"datestamp": "done=bool"}
        self.checkbox5 = {"datestamp": "done=bool"}
        self.checkbox6 = {"datestamp": "done=bool"}
        self.checkbox7 = {"datestamp": "done=bool"}
        self.checkbox8 = {"datestamp": "done=bool"}

    def save_progress(self):
        #save an instance of this class 
        pass
     """
    
washing = Task("washing", "do the washing", 8, 4, "household","20-11-88")


if __name__ == "__main__":
    # note might be worth creating a class to contain all other class so only one thing needs to be instatiated with task tracking / sorting
    ###### Testing ####
    task_tracking = TaskTracking()
    task_archive =  TaskArchive()
    task_non_urgent = TaskNonUrgent()
    task_urgent = TaskUrgent()

    washing = Task("washing", "do the washing", 8, 4, "household","20-11-88")
    cleaning = Task("cleaning", "clean the house", 6, 2, "household","20-11-88")
    # Task.update_ids()
    # note - need some error handling on the date format here.
    # print(cleaning)
    # print(washing)

    # #Task.remove_task(cleaning)

    # print(Task.task_list)
    # print(Task.id_counter)

    TaskTracking.set_display_task(cleaning)


