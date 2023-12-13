
##### REMOVE WHEN FINSHED TESTING ########
import pickle
def load_file(file_name):
    """ generic load local binary file, takes a filename as a string arg, returns none """
    try:
        with open(file_name, "rb") as file:
            loaded_file = pickle.load(file)
            print(f"{file_name} successfully loaded:{loaded_file}")
            return loaded_file
    
    except(FileNotFoundError, pickle.UnpicklingError):
        print(f"Error with {file_name} file load")

def save_file (file_name, variable):
    """ generic save binary file, takes file name as a string and the varialbe you want to save
     returns none """
    try:
        with open(file_name, "wb") as file:
            pickle.dump(variable, file)
        print(f"{variable} successfully saved to '{file_name}'")

    except (PermissionError, FileNotFoundError, pickle.PicklingError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__} - {e}")

##########################################################

############  STACK CLASSES USED FOR SORTING AND STORING TASK OBJECTS ############

class Stack:
    """Used to store/manage tasks
       note these are duplicate task obj in realtion to TaskTracking.all_tasks and are for display and sorting purposes"""
    
    def __init__(self, name):
        self.stack = []
        self.name = name

    def add_task_from_main(self,task, position=None):
        """
        Adds task obj to stack, Can take an optional third argument to add it at a certain position
        IMPORTANTLY removes stack from tasktracking.all_tasks
        """
        if position is not None:
            self.stack.insert(position, task)
            task_tracking.delete_task(task)
            print(f"{task.name} added to {self.name} tracing:class_def,if")


        else:
            self.stack.append(task)
            print(f"{task.name} added to {self.name} tracing:class_def,else")
            task_tracking.delete_task(task)



    def add_task(self, task, position=None):
        """
        Adds task obj to stack, Can take an optional third argument to add it at a certain position.
        """
        if position is not None:
            self.stack.insert(position, task)
        else:
            self.stack.append(task)
            print(f"{task.name} added to {self.name}")

    def remove_task(self, task_name):
        """
        Removes task obj from stack(lst) by task name attribute (str).
        """
        self.stack = [task for task in self.stack if task.name != task_name] 

    def return_task_stack(self):
        return self.stack
    
    def return_stack_names(self):
        """ returns a list of all task names as type(str) """
        stack_names = [x.name for x in self.stack]
        return stack_names

    def print_task_stack(self):
        print(self.name ,self.stack)
        for task in self.stack:
            print(task.name)
    
    def task_exists(self, task)->bool:
        """ Checks if a task exists in the stack """
        return task in self.stack
    
    #might need to put a task obj getter here
        
class ArchiveStack(Stack):
    def __init__(self,name):
        super().__init__(name)
    

    def remove_from_all_stacks(self, task):
        """ Checks for duplicate tasks and removes task from all_stacks list upon adding to the archive stack """
        #list of all stacks
        all_stacks = [task_tracking.task_archive, task_tracking.urgent_stack, task_tracking.non_urgent_task_stack, task_tracking.project_stack, task_tracking]
        
        #while loop to remove them, using task_exists membership method from Stack and Tasktracking classes.
        while any(stack.task_exists(task) for stack in all_stacks):
            for stack in all_stacks:
                if stack.task_exists(task):
                    stack.stack.remove(task)
            
    def add_task_from_main(self,task):
        super().add_task_from_main(task)
        #self.remove_from_all_stacks(task)
        print(f"{task.name} completley removed from all stacks and moved to the archive stack")

####### TASK MANAGEMENT ###########

# TODO -  needs to be a constructor so I can save the class instance on load on start for file persistance of task tracking!
# TODO -  change all the references to old class and cls methods in app.py
# TODO -  add in doc string that all tasks need to be ceated using the create_tasks method to keep track of them.
class TaskTracking:
    def __init__(self):

        self.all_tasks = []
        self.id_counter = 0
        self.display_task = ""

        #pass the var names as args to easily retrieve var names via instance attributes - good alternative to dict of instances
        #might have to use a dict actually due to need an iterable with all the stacks in.
        self.task_archive = ArchiveStack("task_archive") 
        self.urgent_stack = Stack("non_urgent")
        self.non_urgent_task_stack = Stack("non_urgent_task_stack")
        self.project_stack = Stack("project_task_stack") 

        # needed for the getter for selected task callback function can clean this up by jusing a dict of instaces above
        self.all_stacks = [
            self.task_archive,
            self.urgent_stack,
            self.non_urgent_task_stack,
            self.project_stack
        ]

    def create_id(self, task)-> int:
        """ creates an id number and returns it """
        self.all_tasks.append(task)
        self.id_counter += 1
        print(f"""task name: [{task.name}] added to all_tasks -> :{self.all_tasks}""")
        print("id_ counter:", self.id_counter)
        return self.id_counter
    
    def create_task(self, name, description, urgency, importance, category, due_date, project=False, done=False):
        if project:
            task = Project(name, description, urgency, importance, category, due_date, done=done)
        else:
            task = Task(name, description, urgency, importance, category, due_date, done=done)
        return task
    
    def get_task(self,task_name):
        """ pass task name as a string to return that task from the all_task list as an obj """
        for task in self.all_tasks:
            if task.name == task_name:
                print(f"[{task.name}] found and returned")
                return task
            else:
                print(task_name,"not currently in all_tasks list")
        
        for stack in self.all_stacks:
            for task in stack:
                if task.name == task_name:
                    print(f"[{task.name}] found and returned")
                    return task
                else:
                    print(task_name,"not currently in all_stacks list")
    
    def no_of_total_tasks(self)->int:
        return len(self.all_tasks)
    
    def string_list_all_tasks(self):
        string_list = [task.name for task in self.all_tasks] 
        return string_list
    
    def delete_task(self,task):
        """ type(arg) == obj  """
        print("delete_task()","task",task)#<-testing
        print(self.string_list_all_tasks())#<-testing
        self.all_tasks.remove(task)
        print(f"[{task}] successfully deleted from main task list")
        print(self.string_list_all_tasks())#<-testing

    def task_exists(self, task)->bool:
        """ Checks if a task exists in the stack """
        return task in self.all_tasks#<- membership syntax to check if something is in something consicley and return bool
        
    def set_display_task(self, task_obj):
        self.display_task = task_obj

    def get_display_task(self):
        return self.display_task

###############################
task_tracking = TaskTracking()


#keep the instance here so the methods can use it or rename the methods and put it in app.py
#load on app start
#save on app close
#might be a good idea to move stack and tasktracking to another module and import them here. using a callback function in the init of app.py.

######  TASK CLASSES ########
class Task:

    def __init__(self,name ,description,urgency,importance,category,due_date, project=False, done=False ):
        
        
        self.name = name
        self. description = description
        self.urgency = urgency
        self.importance = importance
        self.category = category
        self.due_date = due_date
        self.project = project
        self.done = done 

        self.id_ = task_tracking.create_id(self)

        #task_tracking.create_task(self.name, self.description, self.urgency, self.importance, self.category, self.due_date, project=False, done=False)


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
    # thinking about using a list or stack here that contains all the sub tasks for this project and a class ProjectSubtask
    def __init__(self, name, description, urgency, importance, category, due_date, set_for_this_month=False, project=True, done=False):
        super().__init__(name, description, urgency, importance, category, due_date, project, done)

        self.all_subtasks = {}#<- going to try dict of instaces here, other option is using a getter method that takes names as strings.
    
    def create_subtask(self, name, description, urgency, importance, category, due_date, done=False):
        subtask = ProjectSubtask(name, description, urgency, importance, category, due_date, done=done, parent_project=self)
        self.all_subtasks[name] = subtask #<- add instance with name as key
        subtask.id_ = task_tracking.create_id(subtask)  # Call the create_id method to update all_tasks and create an ID
        return subtask
    
class ProjectSubtask(Task):
    def __init__(self, name, description, urgency, importance, category, due_date,parent_task, project=True, done=False):
        super().__init__(name, description, urgency, importance, category, due_date, project, done)
        self.parent_project_task_inst = parent_task #<- may need this for sorting/browsing may not






#############

# TODO - implement some kind of log, that logs everything printed to the terminal every "session" (console_loggin.py)


###### testing
    


    # note might be worth creating a class to contain all other class so only one thing needs to be instatiated with task tracking / sorting
    
    
    ###### Testing ####

    #testing the saving
    #washing = None
    #cleaning = Task("cleaning", "clean the house", 6, 2, "household","20-11-88")

   # task_tracking.get_task("washing")

    #save_file("task_tracking.pkl",task_tracking)


    #testing the loading
    # task_tracking = load_file("task_tracking.pkl")

    
    # print("main task stack:")
    # task_tracking.main_task_stack.print_task_stack()
    

    # loading task tracking 

if __name__ == "__main__":

    # task_tracking = load_file("task_tracking.pkl")
    # print("testing")
    # washing = task_tracking.get_task("washing")
    # print(task_tracking.all_tasks)
    # task_tracking.set_display_task(washing)
    # print("ran name == main")
    print(task_tracking.all_tasks)

    



    # Task.update_ids()
    # note - need some error handling on the date format here.
    # print(cleaning)
    # print(washing)

    # #Task.remove_task(cleaning)

    # print(Task.task_list)
    # print(Task.id_counter)



