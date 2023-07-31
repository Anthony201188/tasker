
class Task:
    task_list = [] # considering using a deque for this?
    id_counter = -1 
    display_task = ""


    def __init__(self,name ,description,urgency,importance,catagory,due_date, project=False, done=False ):
        
        self.name = name
        self. description = description
        self.urgency = urgency
        self.importance = importance
        self.catagory = catagory
        self.due_date = due_date

        self.project = project
        self.done = done 

        #id tracking implimented to match class attribute count and index position in task_list
        Task.id_counter += 1      
        self.id_ = Task.id_counter      
        Task.task_list.append(self)     

    # used to set the task for display window
    @classmethod    
    def set_display_task(cls, value ):
        cls.display_task = value
    
    @classmethod
    def get_display_task(cls):
        return cls.display_task

    @classmethod                      
    def remove_task(cls, task):
        Task.task_list.remove(task)
        cls.update_ids()

    @classmethod
    def update_ids(cls):
        for index, task in enumerate(cls.task_list):
            task.id_ = index  


    
      
    #String method overidden for testing  
    ##testing## Current task list:{self.task_list}
    ##testing## Task [{self.name}]'s index position in the task list [{self.id_}]
    def __str__(self) -> str:
        return (f"""

                Task name: [{self.name}]
                Task description: [{self.description}]
                Task urgency:[{self.urgency}]
                Task importance:[{self.importance}]
                Task catagory:[{self.catagory}]
                Task due date:[{self.due_date}]
                Task status:Done=[{self.done}]
                """)
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

class Project(Task):
    """ this class is used only if the task is a project it inherits from the project class but allows the adding of sub tasks within that project task """
    # write the class for project here.
    pass


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
    



###### Testing ####
washing = Task("washing", "do the washing", 8, 4, "household","20-11-88")
cleaning = Task("cleaning", "clean the house", 6, 2, "household","20-11-88")
# Task.update_ids()

# print(cleaning)
# print(washing)

# #Task.remove_task(cleaning)

# print(Task.task_list)
# print(Task.id_counter)

Task.set_display_task(cleaning)


