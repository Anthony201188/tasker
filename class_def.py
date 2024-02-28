
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

    def add_task_from_main(self, task, position=None):
        """
        Adds task obj to stack, Can take an optional third argument to add it at a certain position
        IMPORTANT removes stack from tasktracking.all_tasks
        """
        try:
            if position is not None:
                self.stack.insert(position, task)
                task_tracking.delete_task(task)
                print(f"{task.name} added to {self.name}")
            else:
                self.stack.append(task)
                print(f"{task.name} added to {self.name}")
                task_tracking.delete_task(task)
        except ValueError:
            print(f"Error: {task.name} not found in task_tracking. Task not removed from task_tracking.")



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
        """Returns a list of all task names as type(str) if the stack is empty it returns none"""
        
        # Check if self.stack is empty
        if not self.stack: 
            return None  # Return None if self.stack is empty
        
        # Generate the list of task names from self.stack
        stack_names = [x.name for x in self.stack]
        return stack_names

    def print_task_stack(self):
        print(self.name ,self.stack)
        for task in self.stack:
            print(task.name)
    
    def task_exists(self, task)->bool:
        """ Checks if a task exists in the stack """
        return task in self.stack
    
    def get_task(self,task):
        """ Takes a string as and arg and returns the task obj if found in stack else returns none """
        task_to_return = None
        
        for item in self.stack:
            if item.name == task:
                task_to_return = item
        
        return task_to_return
    
    def empty(self):
        """ emptys the stack its called from """
        self.stack = []
    
    #might need to put a task obj getter here
        
class ArchiveStack(Stack):
    def __init__(self,name):
        super().__init__(name)
        self.stack = []
    

    def remove_from_all_stacks(self, task):
        """ Checks for duplicate tasks and removes task from all_stacks list upon adding to the archive stack """
       #TODO - check that all of these take obj not strings as args
        #list of all stacks
        self.all_stacks = [ task_tracking.urgent_stack, task_tracking.non_urgent_task_stack, task_tracking.project_stack, task_tracking]
        
        #while loop to remove them, using task_exists membership method from Stack and Tasktracking classes.
        while True:
            found_in_any_stack = any(stack.task_exists(task) for stack in self.all_stacks)

            for stack in self.all_stacks:
                if stack.task_exists(task):
                    stack.remove_task(task.name)

            if not found_in_any_stack:
                print(f"all instances of task {task.name} found and deleted from all_tacks ")
                break


    
            
    def archive_task(self,task):
        #print the contents of the archive stack before
        print(f"Contents of the Archive stack before:{self.stack}")

        #add task to the archive stack whilst removing it from the task_tracking.all_tasks
        self.add_task_from_main(task)

        #remove the tasks from all_stacks
        self.remove_from_all_stacks(task)

        #print the new archive stack and confirmation
        print(f"Contents of the Archive stack after:{self.stack}")
        print(f"{task.name} completley removed from all stacks and moved to the archive stack")

####### TASK MANAGEMENT ###########

# TODO -  needs to be a constructor so I can save the class instance on load on start for file persistance of task tracking!
# TODO -  change all the references to old class and cls methods in app.py
# TODO -  add in doc string that all tasks need to be ceated using the create_tasks method to keep track of them.
class TaskTracking:
    def __init__(self):

        self.all_tasks = []
        self.all_tasks_temp = []
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
    
    def create_task(self, name, description, urgency, importance, category, due_date, isproject=False, isparent=False, done=False):
        """ Creation of task instances """
        #TODO - add validation and error handling including strong type checking.

        if isproject and isparent:
            task = Project(name, description, urgency, importance, category, due_date, done=done) #<- need to add parent task here?
        elif isproject:
            task = Project.create_subtask(self, name, description, urgency, importance, category, due_date, isproject=True, done=False)#<- needs filtering on the other drop down so sub tasks dont show up there
        else:
            task = Task(name, description, urgency, importance, category, due_date, done=done)
        return task
    
    
    def get_task(self,task_name):
        """ pass task name as a string to return that task from the all_task list as an obj """
        cleaned_task_name = task_name.strip()
        
        for task in self.all_tasks:
            if task.name == cleaned_task_name:
                print(f"[{task.name}] found and returned")
                return task
        else:
            print(task_name,"not currently in [all_tasks] list")
        
        for stack in self.all_stacks:
            for task in stack.stack:
                if task.name == cleaned_task_name:
                    print(f"[{task.name}] found and returned")
                    return task
        else:
            print(task_name,"not currently in [all_stacks] list")
    
    def no_of_total_tasks(self)->int:
        return len(self.all_tasks)
    
    def string_list_all_tasks(self):
        string_list = [task.name for task in self.all_tasks] 
        return string_list
    
    def delete_task(self,task):
        """ type(arg) == obj  """
        #TODO - Include find and remove for "all_task_stacks"
        print("delete_task()","task",task)#<-testing
        print(self.string_list_all_tasks())#<-testing
        self.all_tasks.remove(task)
        print(f"[{task}] successfully deleted from main task list")
        print(self.string_list_all_tasks())#<-testing

    def return_all_stacks_combined(self):
        """ returns the current contents of all stacks as a single list """
        combined_list = []
        for stack in self.all_stacks:
            combined_list.extend(stack.stack)

        print(f"combined_stacks:[{combined_list}]")
        return combined_list


    
    def delete_task_everywhere(self,task):
        """ Removes a single task(obj) from both the all_tasks list and all_stacks
        Note:the same as the archive stack method 'remove_from_all_stacks()'
        """
        print("delete_task_everywhere() called")
        
        try:
            self.all_tasks.remove(task)
            print(f"[{task.name}] found in all_tasks and successfully deleted.")
        except ValueError as e:
            print(f"Error:[{task.name}] not in all_tasks, searching all_stacks...")
            try:
                all_stacks = self.return_all_stacks_combined()
                if task in all_stacks:
                    task.delete_self()
            except ValueError as e:
                print(f"Error:[{task.name}] not in all_stacks or all_tasks, can't be deleted")


    def task_exists(self, task)->bool:
        """ Checks if a task exists in the stack """
        return task in self.all_tasks#<- membership syntax to check if something is in something consicley and return bool
        
    def set_display_task(self, task_obj):
        self.display_task = task_obj

    def get_display_task(self):
        return self.display_task
    
    def return_all_parent_project_names(self):
        """Returns names of all parent projects in all_stacks and all_tasks."""
        project_task_names = []

        for task in self.all_tasks:
            if task.isproject and not isinstance(task, ProjectSubTask):
                project_task_names.append(task.name)

        for stack in self.all_stacks:
            for task in stack.stack:
                if task.isproject and not isinstance(task, ProjectSubTask):
                    project_task_names.append(task.name)
        print("testing project_task_names",project_task_names)
        return project_task_names
    
    def empty_all(self):
        """ deletes entire contents of all tasks in task_tracking """
        self.all_tasks = []
        print(f"self.all_tasks now empty[{self.all_tasks}]")
        for stack in self.all_stacks:
            stack.stack = []
        print(f"all_stacks now empty: {[f'{stack.name}:{stack.stack}' for stack in self.all_stacks]}")



###############################
task_tracking = TaskTracking()


#keep the instance here so the methods can use it or rename the methods and put it in app.py
#load on app start
#save on app close
#might be a good idea to move stack and tasktracking to another module and import them here. using a callback function in the init of app.py.

######  TASK CLASSES ########
class Task:

    def __init__(self,name ,description,urgency,importance,category,due_date, isproject=False, done=False ):
        
        
        self.name = name
        self. description = description
        self.urgency = urgency
        self.importance = importance
        self.category = category
        self.due_date = due_date
        self.isproject = isproject
        self.done = done 

        self.id_ = task_tracking.create_id(self)

        #task_tracking.create_task(self.name, self.description, self.urgency, self.importance, self.category, self.due_date, project=False, done=False)

    def print_attributes(self,obj):
        """ prints all attributes of an instance object """
        for attr_name in vars(obj):
            attr_value = getattr(obj, attr_name)
            print(f"{attr_name}: {attr_value}")

    def __str__(self) -> str:
        return (f"""
                Task name: [{self.name}]
                Task description: [{self.description}]
                Task urgency:[{self.urgency}]
                Task importance:[{self.importance}]
                Task catagory:[{self.category}]
                Task due date:[{self.due_date}]
                Task status:Done=[{self.done}]
                Task is a project:[{self.isproject}]
                Task is a parent :[{isinstance(self, Project)}]
                Task is a sub task: [{isinstance(self, ProjectSubTask)}]
                Task id_:[{self.id_}]
                """)
    
    def update_attributes(self, **kwargs):
        """ set any number of attributes for task instance objects similtaiously
            use: 'obj.update_attributes(attribute1=20)'
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        #print updated attributes and values 
        print(f"Task [{self.name}] the following attributes have been successfully updated:")
        if not kwargs:
            print("update_attributes **kwargs empty",kwargs)
        for key, value in kwargs.items():
            print(f"  {key}: {value}")

    def delete_self(self):
        del self
        print(f"{self.name} deleted.")


class Project(Task):
    """ this class is used only if the task is a project it inherits from the project class but allows the adding of sub tasks within that project task """
    # thinking about using a list or stack here that contains all the sub tasks for this project and a class ProjectSubtask
    def __init__(self, name, description, urgency, importance, category, due_date, isproject=True,isparent=True, done=False): # replace all "isproject" "isparent" with "isinstance(self, Project)" or "isinstance(self, ProjectSubTask)"
        super().__init__(name, description, urgency, importance, category, due_date, isproject, done)

        self.all_subtasks = {}#<- going to try dict of instaces here, other option is using a getter method that takes names as strings.
        self.isparent = isparent#<- can probs remove this and do this implicitly later


    #the method below should I just pass it an instance of Project class and then inherit all the attributes and the parent_project would = the instance of the Project class instance
    def create_subtask(self, name, description, urgency, importance, category, due_date, done=False):
        subtask = ProjectSubTask(name, description, urgency, importance, category, due_date, done=done, parent_project=self)
        self.all_subtasks[name] = subtask #<- add instance with name as key
        subtask.id_ = task_tracking.create_id(subtask)  # Call the create_id method to update all_tasks and create an ID
        return subtask
    
class ProjectSubTask(Task):
    def __init__(self, name, description, urgency, importance, category, due_date, parent_project , isproject=True, done=False):
        super().__init__(name, description, urgency, importance, category, due_date, isproject, done)
        self.parent_project_task_inst = parent_project #<- may need this for sorting/browsing may not






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



