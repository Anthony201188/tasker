import class_def 
import data_structure
import pickle
import customtkinter as ctk
import time
import calendar
import os
from time import sleep
from link_click import ClickableLinkLabel
from algo import main as algo
from urgent_algo import sort_urgent_tasks


########################################  UTILS #####################################
""" file persistance used to save load and update stored data on opening of app """

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

def on_close():

    # save time on close for elapse
    closing_time = time.time()
    save_file("closing_date.pkl", closing_time)
    print(f"App closed at epoch time: {closing_time}")

    # save habit1/2 on close
    app.my_frame.save_habits()

    #save remedial swtich postions on close
    save_file("remedial_switch_positions.pkl",app.my_frame2.loaded_remedial_positions)

    # save daily tasks
    print("daily tasks set:",app.my_frame2.daily_tasks_set)#<- testing
    if app.my_frame2.daily_tasks_set:
        app.my_frame2.save_daily_tasks()    

    # save duration on close
    app.my_frame.save_duration(app.my_frame.get_current_duration())
    
    app.destroy()  # Close the CTKinter app


# TODO - make this generic and use it in all task list widgets.
""" def populate_task_list(self, task_stack):
        ''' populates the task list with all relevant, takes the task_stack(obj) as arg '''

    # Insert task names
        print("task_stack type:", type(task_stack))
        print("TESTING WORKING")
        task_names = task_stack.return_stack_names()

        if task_names:
            for task_name in task_names:
                self.textbox.insert("end", task_name, "\n")
            self.textbox.configure(state="disabled")
            print("Tasks text successfully inserted")
        else:
            # Insert alt text into box
            self.textbox.insert("0.0", "Task list is empty. No tasks to display.")
            self.textbox.configure(state="disabled")
        
        # set up the recursive
        self.after(1000,self.populate_task_list(class_def.task_tracking.non_urgent_task_stack)) """


#####################################################################################
#TODO - make all ##### banners match data_structure.py style
###################### DEFINING FRAMES AND WIDGETS ###################################
#Habit Tasks
class MyFrame(ctk.CTkFrame):

    def __init__(self, master,text, width, height, app_instance):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # reference to the App instance for later use
        self.app_instance = app_instance #<-dependency injection

        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Remaining days label
        self.label2 = ctk.CTkLabel(self,anchor=ctk.S, text="Remaing days untill end of habit forming",width=60, height=60)
        self.label2.grid(row=3, column=0, padx=10, pady=5)

        #Number of days label
        self.label_number_of_days_remaining = ctk.CTkLabel(self,anchor=ctk.S, text="0",width=60, height=60) 
        self.label_number_of_days_remaining.grid(row=3, column=2, padx=10, pady=5)

        #Entries
        self.habit1_set_var = ctk.BooleanVar(value=False)
        self.entry_habit1 = ctk.CTkEntry(self,placeholder_text="Habit1",width=180)
        self.entry_habit1.grid(row=1, column=0, padx=10, pady=10)
        
        self.habit2_set_var = ctk.BooleanVar(value=False)
        self.entry_habit2 = ctk.CTkEntry(self,placeholder_text="Habit2",width=180)
        self.entry_habit2.grid(row=2, column=0, padx=10, pady=10)

        self.entry_duration = ctk.CTkEntry(self, placeholder_text="Duration",width=70)
        self.entry_duration.place(x=350,y=100)

        self.all_habit_boolvars = [self.habit1_set_var, self.habit2_set_var]

        #habits set timestamp
        self.habit_set_timestamp = "timestamp-placeholder" #<- needs file persistance preferable if using db create a table specifically for file persistance

        #set duration var
        self.set_duration_var = ""


        #Buttons
        self.button = ctk.CTkButton(self, text="set habits and duration",command=lambda:(self.toggle_habits_set(),self.set_habits_and_duration()) ,height=28, width=28 ) 
        self.button.grid(row=1, column=3, padx=20)

        # TODO - dont need this toggle option above  as it will only ever bet set not "unset"
        #TODO - remove once button placement is correct
        #self.button2 = ctk.CTkButton(self, text="set duration",command=self.xxxxxx, height=28, width=28 ) 
        #self.button2.grid(row=2, column=3, padx=20)

        #Checkboxes
        self.habit1_check_var = ctk.BooleanVar(value=False)  
        self.habit1_check = ctk.CTkCheckBox(self, text="Done", variable=self.habit1_check_var,fg_color="black", onvalue=True, offvalue=False) 
        self.habit1_check.grid(row=1, column=2)

        self.habit2_check_var2 = ctk.BooleanVar(value=False)  
        self.habit2_check2 = ctk.CTkCheckBox(self, text="Done", variable=self.habit2_check_var2,fg_color="black", onvalue=True, offvalue=False) 
        self.habit2_check2.grid(row=2, column=2)


        #TODO - remove - Load the habits
        #self.habit1 =load_file("habit1.pkl")
        #self.habit2 = load_file("habit2.pkl")

        # configure grid system
        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(2, weight=1)

        ############## on-start control logic ################

        ##duration
        #load duration
        self.loaded_duration = self.load_duration() 

        #updates the duration based on elapsed time then schedules next update for 24hrs
        self.updated_duration = self.update_duration(self.loaded_duration) #<- needs to return the updatded duration so theres no errors on non zero load -> not resetting entries

        #gets the duration and saves it locally
        self.save_duration(self.get_current_duration())

        # on-close function edited for save duration for file persistance 
        
        ## habits
        #load the habit files as a tuple
        self.loaded_habits = self.load_habits()

        # re-set the entries or load the loaded vals into the habit1/2 entries.
        if self.updated_duration == 0:
            self.reset_habits()
        else:
            self.set_habits(self.loaded_habits)

    
    ############## methods ##############
    #get set duration var
    def get_set_duration_var(self):
        """ returns the self.set_duration_var as a tuple(str,) for the DB """
        return tuple(str(self.set_duration_var),)        

    #get days remaining
    def get_days_remaining(self):
        """ returns the number of days remaining as a tuple(str,) for the DB """
        days_remaining = self.get_current_duration()
        return tuple(str(days_remaining,))

            
    #get habitset_timestamp
    def get_habit_set_timestamp(self):
        """ return the last set time of the last habit setting as a datetime string in ISO 8601 """
        return self.habit_set_timestamp

    #habit functions
    def load_habits(self)->tuple:
        """ Loads duration from "habit1/2.pkl files" and returns them as a tuple. """
        self.text1 = load_file("habit1.pkl")
        self.text2 = load_file("habit2.pkl")
        return self.text1, self.text2  #<-returns tuple

    def set_habits(self, tuple_of_strings):
        """ Takes a tuple of two strings, unpacks them and sets them to their respective labels.
        Also then disables the entreis and changes the border weight to show entries as 'set' """
        
        #Remove current text
        self.entry_habit1.delete(0,"end")
        self.entry_habit2.delete(0,"end")
        print("deleting entries now")

        #unpack tuple
        self.text1 ,self.text2 = tuple_of_strings
        print("habit tuple:", self.text1, self.text2)
        
        #insert text to labels
        self.entry_habit1.insert(0,self.text1)
        self.entry_habit2.insert(0,self.text2)
        
        #disables the entries and thickens the border to show that they are 'set'
        self.entry_habit1.configure(state="disabled", border_width=3, border_color="black")
        self.entry_habit2.configure(state="disabled", border_width=3, border_color="black")

        #toggle the habits
        #self.toggle_habits_set()
        print("habit setting completed!")

    def save_habits(self):
        """ saves whatever text is currently in the habit1/2 entries and saves it in a serial .pkl file locally """

        #gets the entry text and saves it
        habit1 = self.entry_habit1.get()
        habit2 = self.entry_habit2.get()
        save_file("habit1.pkl", habit1)
        save_file("habit2.pkl", habit2)

    def get_habits(self)-> tuple:
        """ gets the string val currently in enties habit1/2, returns a tuple of local vals """
        
        #get the text in the habits entries
        habit1 = self.entry_habit1.get()
        habit2 = self.entry_habit2.get()
        return habit1, habit2

    def get_habits_names(self):
        """ returns a list of entry names and list of entry content used for finish for the day button press"""
        self.entry_content = []
        self.entry_names = ["habit1","habit2"]

        #get the text in the habits entries
        self.entry_content.append(self.entry_habit1.get())
        self.entry_content.append(self.entry_habit2.get())

        print(f"Entry content:{self.entry_content},Entry names:{self.entry_names}")

        return self.entry_names, self.entry_content 
    
    def toggle_habits_set(self):
        """ toggle the bool_vars indicating if either of the habit entries have been set """

        #check if either of the set vars are truthy
        #indicating the habits have been set to check for toggling values when already set
        if self.habit1_set_var.get() or self.habit2_set_var.get():
            pass
        

        else:
            #gets habits to only set if they are truthy
            habit1, habit2 = self.get_habits()

            # Toggles the set BooleanVars for each entry and prints the
            if habit1:
                new_value = not self.habit1_set_var.get()
                self.habit1_set_var.set(new_value)
                self.habit_set_timestamp = data_structure.get_current_time()
                print(f"Habit1 set = {new_value}")

            if habit2:
                new_value = not self.habit2_set_var.get()
                self.habit2_set_var.set(new_value)
                self.habit_set_timestamp = data_structure.get_current_time()
                print(f"Habit2 set = {new_value}")



    
    def reset_habits(self):
        """ enables the habit entries and resets the habit1/2 persistance files back to default text """
        
        #enables the entries and reduces border width and colour to show'reset'
        self.entry_habit1.configure(state="normal", border_width=1, border_color="grey")
        self.entry_habit2.configure(state="normal", border_width=1, border_color="grey")
        
        # entry 1 delete and reset default text
        self.entry_habit1.delete(0,-1)
        self.entry_habit1.insert(0, "habit1")
        
        # entry 2 delete and reset default text
        self.entry_habit2.delete(0,-1)
        self.entry_habit2.insert(0, "habit2")

        self.save_habits()

    #duration functions
    def load_duration(self):
        """ load_file method specifically for loading 'duration' file, returns duration"""

        return load_file("duration.pkl")
        
    def set_duration(self, duration_to_set):
        """ takes an integers as an arg and sets the duration label to it"""


        self.label_number_of_days_remaining.configure (text = duration_to_set)
        self.set_duration_var = duration_to_set 
        print(f"self.set_duration_var set to :{duration_to_set}")
        print (f"habit duration set to:{duration_to_set}")


    def get_entry_duration(self)->str:
        """ gets whatever is in the 'duration' entry, returns it as an str """
        self.duration = self.entry_duration.get()
        return self.duration            
    
    def get_current_duration(self)-> int:
        """ gets whatever is currently set as the remaining days label and returns it an int. """
        current_duration = self.label_number_of_days_remaining.cget("text")
        #testing
        print("current_duration:",current_duration)
        return int(current_duration)
    
    def schedule_update(self, duration_hours, function):
        """Schedule the passed function  to run after the specified number of hours."""
        milliseconds = duration_hours * 60 * 60 * 1000
        self.after(milliseconds, function)

    def update_duration(self, loaded_duration):
        """takes the loaded duration as an arg(int)
        updates the duration using the elapsed days and set duration functions,
        finally scheduling the next update for 24 hours time """

        # Initialize updated_duration with a default value, stops unbounderror due to else block
        updated_duration = 0

        # Update the duration based on elapsed days
        self.whole_elapsed_days = self.get_elapsed_days()
        print("Number of days to deduct from duration:",self.whole_elapsed_days)

        # set updated duration
        print("Current loaded duration:", loaded_duration)
        if loaded_duration < 0 or (loaded_duration - self.whole_elapsed_days) < 0: #<-updated this again to account for differences in loaded and elapsed days that are negative                                                    
            updated_duration = 0
        else:
            updated_duration = loaded_duration - self.whole_elapsed_days
            self.set_duration(updated_duration)

        # Schedule next update
        self.schedule_update(24, self.update_duration)

        #testing
        print("returnedupdated_duration:", updated_duration) 

        return updated_duration

    def save_duration(self, duration_to_save):
        """ Takes a single int as a durtion, saves that to the serial 'duration.pkl' file locally """
        save_file("duration.pkl", duration_to_save)

    def get_elapsed_days(self)->int:
        """  finds the number of elapsed days between app open and close, uses the diffference between file 'closing_date.pkl'  """
        # get the loaded closing date (float)
        self.loaded_date = load_file("closing_date.pkl")

        # set the start date for duration calculation (float)
        self.start_date = time.time()

        # Calulate the difference between closing date and date now.
        self.difference = self.start_date - self.loaded_date
        print("Float difference in seconds", self.difference)

        # Extract the number of whole days from the time float.
        self.elapse = round(self.difference / (24 * 60 * 60))  # 24hrs * 60m * 60s #<-should change duration by 1 @ 1400 CET as the epoch time runs from UTC
        print("Elapsed epoch days:",self.elapse) #should be a single number of days as an int e.g. 1 or 2
        return self.elapse
    
    #combined functions
    def set_habits_and_duration(self):
        """ gets the string val currently in enties habit1/2, then 'sets' the entries as disabled,
            saves the habits then does the same with the required duration  """
        ##logic
        current_duration = self.get_current_duration()
        if current_duration == 0:
            ##habits
            #gets the habits in the current entries returns tuple.
            habits = self.get_habits()

            #sets habits
            self.set_habits(habits)

            #saves habits locally
            self.save_habits()

            ##duration
            #get and set the duration
            test_duration = self.get_entry_duration()
            self.set_duration(test_duration) 

        else:
            print("Current habit duration not elapsed, please wait until duraiton = 0")

    def get_habit_done_flags(self):
        """ get the done flags and return them as integers representing boool vals for DB """
        done_flag_tuple = []
        
        if self.habit1_check_var.get():
            done_flag_tuple.append("1")
        else:
            done_flag_tuple.append("0")
        if self.habit2_check_var2.get():
            done_flag_tuple.append("1")
        else:
            done_flag_tuple.append("0")
        
        return tuple(done_flag_tuple)

        

#Todays Tasks
class MyFrame2(ctk.CTkFrame):
    def __init__(self, master,text, width, height, app_instance):
        super().__init__(master, width, height)

        # Reference to the App instance for later use
        self.app_instance = app_instance

        # Set the title and frame size on instantiation
        self.val = text
        self.val2 = width
        self.val3 = height


        # Labels
        self.label = ctk.CTkLabel(self, text=self.val)
        self.label.place(x=15, y=5)

        self.label_done = ctk.CTkLabel(self, text="Done", font=("",9))
        self.label_done.place(x=296, y=5)

        self.label_remedial = ctk.CTkLabel(self, text="Remedial \n work required",font=("",9))
        self.label_remedial.place(x=335, y=5)


        # Entries
        self.entry_set_var = ctk.BooleanVar(value=False)
        self.entry = ctk.CTkEntry(self,placeholder_text="Project", border_color="green",text_color="green", width=280)
        self.entry.place(x=10, y=35)

        self.entry2_set_var = ctk.BooleanVar(value=False)
        self.entry2 = ctk.CTkEntry(self,placeholder_text="Urgent",border_color="red",text_color="red", width=280)
        self.entry2.place(x=10, y=85)

        self.entry3_set_var = ctk.BooleanVar(value=False)
        self.entry3 = ctk.CTkEntry(self,placeholder_text="Urgent",border_color="red",text_color="red" , width=280)
        self.entry3.place(x=10, y=118)
       
        self.entry4_set_var = ctk.BooleanVar(value=False)
        self.entry4 = ctk.CTkEntry(self,border_color="blue",text_color="blue",placeholder_text="Task1",width=280)
        self.entry4.place(x=10, y=160)

        self.entry5_set_var = ctk.BooleanVar(value=False)
        self.entry5 = ctk.CTkEntry(self,border_color="blue",text_color="blue",placeholder_text="Task2",width=280)
        self.entry5.place(x=10, y=193)


        #list of all entries
        self.all_entries = [self.entry, self.entry2, self.entry3, self.entry4, self.entry5]
        self.all_set_entry_vars = [
            self.entry_set_var,
            self.entry2_set_var,
            self.entry3_set_var,
            self.entry4_set_var,
            self.entry5_set_var
            ]

        #dict of all entries and set vars
        self.entry_var_dict = dict(zip(self.all_entries, self.all_set_entry_vars))

        #Buttons
        self.button_suggest = ctk.CTkButton(self, text="Easy day toggle",command=self.easy_day_toggle, height=28, width=28 ) 
        self.button_suggest.place(x=405, y=33)
        
        self.button_sort = ctk.CTkButton(self, text="sort all tasks",fg_color="dark blue",command= lambda:(self.sort_all_tasks(),MyFrame5.populate_task_list(app.my_frame5, class_def.task_tracking.non_urgent_task_stack),MyFrame5.populate_task_list(app.my_frame5v3, class_def.task_tracking.urgent_stack)), height=28, width=45 ) # need to shorten the lamda function here by combining the updating of all funcitions somehwere!
        self.button_sort.place(x=405, y=65)

        self.button_suggest = ctk.CTkButton(self, text="suggest",command=self.suggest_todays_tasks, height=28, width=28 ) 
        self.button_suggest.place(x=405,y=97)   
          
        self.button_set = ctk.CTkButton(self, text="set",command=self.set_entries_callback, height=28, width=50 ) 
        self.button_set.place(x=405,y=160)

        self.button_clear = ctk.CTkButton(self, text="clear all",fg_color="light blue",command=lambda:(self.toggle_set_entry_var(),self.reset_clear()), height=28, width=45 ) 
        self.button_clear.place(x=405, y=193)


        #Checkboxes 
        self.project_check_var = ctk.BooleanVar(value=False) 
        self.check = ctk.CTkCheckBox(self,checkbox_height=28,checkbox_width=28,text=None, variable=self.project_check_var,fg_color="green",border_color="green", onvalue=True, offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.check.place(x=295, y=35)

        #self.entry.lift(aboveThis=self.check)

        self.urgent_check1_var = ctk.BooleanVar(value=False)  
        self.urgent_check1 = ctk.CTkCheckBox(self,checkbox_height=28,checkbox_width=28, text=None, variable=self.urgent_check1_var, onvalue=True,fg_color="red", border_color="red", offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.urgent_check1.place(x=295, y=85)
  
        self.urgent_check2_var = ctk.BooleanVar(value=False)  
        self.urgent_check2 = ctk.CTkCheckBox(self,checkbox_height=28,checkbox_width=28, text=None, variable=self.urgent_check2_var, onvalue=True,fg_color="red", border_color="red", offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.urgent_check2.place(x=295, y=120)   

        self.non_urgent_check1_var = ctk.BooleanVar(value=False)  
        self.non_urgent_check1 = ctk.CTkCheckBox(self,checkbox_height=28,checkbox_width=28, text=None, variable=self.non_urgent_check1_var, onvalue=True, border_color="blue",offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.non_urgent_check1.place(x=295, y=160)  

        self.non_urgent_check2_var = ctk.BooleanVar(value=False)  
        self.non_urgent_check2 = ctk.CTkCheckBox(self,checkbox_height=28,checkbox_width=28, text=None, variable=self.non_urgent_check2_var, onvalue=True, border_color="blue",offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.non_urgent_check2.place(x=295, y=193)



        #Remedial work switches 
        #project
        self.project_remedial_switch_var = ctk.BooleanVar(value=False)
        self.project_remedial_switch = ctk.CTkSwitch(
            self,variable=self.project_remedial_switch_var,
            onvalue=True, offvalue=False ,text=None, fg_color="green",
            command=lambda  :(
                self.toggle_colour(self.project_remedial_switch_var,(self.entry, self.check),"green","light green"),
                self.update_remedial_original_entry_content(),
                self.update_remedial_switch_positions()))
        self.project_remedial_switch.place(x=350,y=35)

        #urgent1
        self.urgent1_remedial_switch_var = ctk.BooleanVar(value=False)
        self.urgent1_remedial_switch = ctk.CTkSwitch(
            self,variable=self.urgent1_remedial_switch_var,
            onvalue=True, offvalue=False, text=None, fg_color="red",
            command=lambda :(
                self.toggle_colour(self.urgent1_remedial_switch_var,(self.entry2, self.urgent_check1),"red","pink"),
                self.update_remedial_original_entry_content(),
                self.update_remedial_switch_positions()))
        self.urgent1_remedial_switch.place(x=350,y=85)

        #urgent2
        self.urgent2_remedial_switch_var = ctk.BooleanVar(value=False)
        self.urgent2_remedial_switch = ctk.CTkSwitch(
            self,variable=self.urgent2_remedial_switch_var,
            onvalue=True, offvalue=False, text=None,fg_color="red",
            command=lambda :(self.toggle_colour(self.urgent2_remedial_switch_var,(self.entry3, self.urgent_check2),"red","pink"),
                             self.update_remedial_original_entry_content(),
                             self.update_remedial_switch_positions()))
        self.urgent2_remedial_switch.place(x=350,y=120)

        #urgent1
        self.non_urgent1_remedial_switch_var = ctk.BooleanVar(value=False)
        self.non_urgent1_remedial_switch = ctk.CTkSwitch(
            self,variable=self.non_urgent1_remedial_switch_var,
            onvalue=True, offvalue=False ,text=None,fg_color="blue",
            command=lambda :(self.toggle_colour(self.non_urgent1_remedial_switch_var,(self.entry4, self.non_urgent_check1),"blue","light blue"),
                             self.update_remedial_original_entry_content(),
                             self.update_remedial_switch_positions()))
        self.non_urgent1_remedial_switch.place(x=350,y=160)        
        
        #urgent2
        self.non_urgent2_remedial_switch_var = ctk.BooleanVar(value=False)
        self.non_urgent2_remedial_switch = ctk.CTkSwitch(
            self,variable=self.non_urgent2_remedial_switch_var,
            onvalue=True, offvalue=False, fg_color="blue", text=None,
            command=lambda :(self.toggle_colour(self.non_urgent2_remedial_switch_var,(self.entry5, self.non_urgent_check2),"blue","light blue"),
                             self.update_remedial_original_entry_content(),
                             self.update_remedial_switch_positions()))
        self.non_urgent2_remedial_switch.place(x=350,y=193)  

        #remedial switch vars
        self.all_remedial_switch_vars = [
        self.project_remedial_switch_var,
        self.urgent1_remedial_switch_var,
        self.urgent2_remedial_switch_var,
        self.non_urgent1_remedial_switch_var,
        self.non_urgent2_remedial_switch_var,
        ]

        #remedial switch vars
        self.all_remedial_switches = [
        self.project_remedial_switch,
        self.urgent1_remedial_switch,
        self.urgent2_remedial_switch,
        self.non_urgent1_remedial_switch,
        self.non_urgent2_remedial_switch,
        ]


        #dict of widgets to toggle and there place locations as vals
        self.easy_day_widgets_to_toggle = {
            #switches
            self.project_remedial_switch:"350,35",
            self.urgent2_remedial_switch:"350,185",
            self.non_urgent2_remedial_switch:"350,120",
            #checkboxes
            self.check:"295,35",
            self.urgent_check2:"295,120",
            self.non_urgent_check2:"295,193",
            #entries
            self.entry:"10,35",
            self.entry3:"10,118",
            self.entry5:"10,193"
            }

        # varible for all entreis and corresponding switch vars
        self.entries_and_switch_vars_dict = {}

        #define a dict for the remeidal tasks original content 
        self.original_remedial_content = None

        #define a set var for Todays tasks
        self.daily_tasks_set = False   

        #define a toggle var for easy day
        self.easy_day_toggle_var = False

        ############ on-start control logic ###########
        #TODO - some file peristance for the entries onces they are set to save on clos
        #TODO - might need to edit this method to work with a list of dictionaries created via the 'save_daily_tasks' method.
        #TODO - tidy the below up when its well tested
        
        self.loaded_entries = []

        #load pickled file
        daily_task_entry_lst = load_file("daily_task_entry_lst.pkl")


        #select entry dicts to pseudo-load, shouldnt  as only truthy values should be stored in file double filtering not bad.
        for dict_obj in daily_task_entry_lst:
            if dict_obj["load_on_start"]: #checks if entry dict "load_on_start" value is truthy 
                self.loaded_entries.append(dict_obj)

        print(f"Daily task entries successfully loaded: {self.loaded_entries}")

        #create a list of the content to load and the entry name to load to
        self.loaded_entires_content = [value["content"] for value in self.loaded_entries]
        self.loaded_entries_name = [value["entry_name"] for value in self.loaded_entries] 

        #set content to entries 
        self.insert_tasks(self.loaded_entires_content, self.loaded_entries_name )

        #lock entries
        self.set_entries_on_start()

        #switch postion file persistance
        try:
            self.loaded_remedial_positions = load_file("remedial_switch_positions.pkl")
        except EOFError as e:
            print(f"Error:{e}")
            print("remedial_switch_positions.pkl doesnt exists, creating file now!")

        #account for first time start with no file
        if not self.loaded_remedial_positions:
            switch_positions = self.update_remedial_switch_positions()
            print("switch_positions",switch_positions)
            save_file("remedial_switch_positions.pkl",switch_positions)
            self.loaded_remedial_positions = switch_positions

        
        #de-bugging
        print("loaded_remedial_positions type",type(self.loaded_remedial_positions))
        print("remdial switch vars type",type(self.all_remedial_switch_vars))
        zipped = list(zip(self.loaded_remedial_positions,self.all_remedial_switches)) # zipped returns iterator object must be set to var to print
        print("zipped bools and switch objs:",zipped)


        #set the entries if needed on start
        for position, switch in zip(self.loaded_remedial_positions, self.all_remedial_switches):
            if position:
                switch.toggle()
                self.set_remedial_on_start()


################ methods ######################
        
    def get_entry_name(self,entry):
        """ returns the name of an entry """
      
        entry_names = {
            self.entry:"project",
            self.entry2:"urgent1",
            self.entry3:"urgent2",
            self.entry4:"nonurgent1",
            self.entry5:"nonurgent2",
        }
        
        return entry_names[entry]

    
    def remedial_switch_capture(self,entries, from_button=False)->dict:
        """ takes a dict of entries and bool vars, if bool is truthy, 
        returns the same but with their contents and not the values
        takes: {entry2:True}
        returns: {entry2:"some text here"}
        note: from_button default val ensures when this function
        is called from finish for the day button the entry isnt unlocked
        """

        captured_entries = {}

        #key and value both objects #  delete this adfter testing
        print("original-entries",entries)

        for entry, bool_var in entries.items():
            if entry and bool_var:
                #if you want obj not string name swap below
                #captured_entries[entry] = entry.get()
                captured_entries[self.get_entry_name(entry)] = entry.get()
                #conditionaly unset entry and bool var here
                if not from_button:
                    self.unset_unlock(entry) 

        #this returns obj, content
        print("original_entry_content returned from function", captured_entries)

        return captured_entries
    
    def update_remedial_switch_positions(self):
        """ updated the self.loded_swtich_positions list every time a switch is thrown """
        self.loaded_remedial_positions = [bool_var.get() for bool_var in self.all_remedial_switch_vars]
        return self.loaded_remedial_positions
   
    
    def update_entries_dict(self):
        """ update the 'self.entries_and_switch_var' dict """

        self.entries_and_switch_vars_dict= {
            self.entry:self.project_remedial_switch_var.get(),
            self.entry2:self.urgent1_remedial_switch.get(),
            self.entry3:self.urgent2_remedial_switch_var.get(),
            self.entry4:self.non_urgent1_remedial_switch_var.get(),
            self.entry5:self.non_urgent2_remedial_switch_var.get()
        }
    

        print("updated-> self.entries dict ",self.entries_and_switch_vars_dict)
        
        return self.entries_and_switch_vars_dict

    
    def update_remedial_original_entry_content(self ,from_button=False):
        """ updates the variable original_remedial_content each time a switch is switched! """

        #update the entries dict
        self.update_entries_dict()
    
        #pass the updated entries_dict to remedial_switch_capture
        self.original_remedial_content = self.remedial_switch_capture(self.entries_and_switch_vars_dict, from_button)
        
        print("global var - self.original_remedial_content", self.original_remedial_content)

        return self.original_remedial_content

    
    def toggle_colour(self,toggle_var, widgets, original_colour, new_colour):
        """ Toggles the colour of switches and entries between original and new colours.
            Switches must be every second value in the tuple e.g (entry, switch, entry, switch).
        """
        toggle = toggle_var.get()
        print("toggle var:",toggle)

        
        if len(widgets) <= 2 and toggle:
            widgets[0].configure(border_color=new_colour,text_color=new_colour  )
            widgets[1].configure(border_color=new_colour )
        
        elif len(widgets) <=2:
           widgets[0].configure(border_color=original_colour,text_color=original_colour  )
           widgets[1].configure(border_color=original_colour )
        
        elif toggle:
            for index, item in enumerate(widgets):
                if index % 2 == 0:
                    item.configure(border_color=new_colour)
                else:
                    item.configure(border_color=new_colour, text_color=new_colour)
        
        else:
            for index, item in enumerate(widgets):
                if index % 2 == 0:
                    item.configure(border_color=original_colour)
                else:
                    item.configure(border_color=original_colour, text_color=original_colour)

    
    def easy_day_toggle(self):
        #toggle the var to the opposite bool 
        self.easy_day_toggle_var = not self.easy_day_toggle_var

        if self.easy_day_toggle_var:
             for key in self.easy_day_widgets_to_toggle.keys():
                key.place_forget()
            
        else:
            #place all said widgets here
            for key, value in self.easy_day_widgets_to_toggle.items():
                # Splitting the string into x and y coordinates
                x, y = map(int, value.split(','))

                # Placing the widget using the extracted coordinates
                key.place(x=x, y=y)

    
    def suggest_non_urgent(self):
        """ takes the top two tasks from the non-urgent task list and puts them into the entries """

        #Access the instance from App class
        my_frame5_instance = self.app_instance.my_frame5
        
        #get the top 2 tasks from app.my_frame5 (Non-urgent task list)
        top_tasks = self.get_top_tasks(my_frame5_instance,2)
        print("Non-urgent top tasks:" ,top_tasks)

        #insert these tasks into the selected entries
        self.insert_tasks(top_tasks,["entry4", "entry5"]) # Non-urgent task entries


    def suggest_urgent(self):
        """ takes the top two tasks from the urgent task list and puts them into the entries """

        #Access the instance from App class
        my_frame5v3_instance = self.app_instance.my_frame5v3
        
        #get the top 2 tasks from app.my_frame5 (Non-urgent task list)
        top_tasks = self.get_top_tasks(my_frame5v3_instance,2)
        print("Urgent top tasks:" ,top_tasks)

        #insert these tasks into the selected entries
        self.insert_tasks(top_tasks,["entry2", "entry3"])


    def suggest_project(self):
        """ takes the top task from the urgent task list and puts it into the entry """

        #Access the instance from App class
        my_frame5v2_instance = self.app_instance.my_frame5v2
        
        #get the top 2 tasks from app.my_frame5 (Non-urgent task list)
        top_task = self.get_top_tasks(my_frame5v2_instance,1)
        print("Project top tasks:" ,top_task)

        #insert these tasks into the selected entries
        self.insert_tasks(top_task,["entry"]) #<- none passed here as a tuple of 1 doesnt seem to count as a tuple its just a string!


    def suggest_todays_tasks(self): # split into sub-functions
        """ 
        Takes x1 project and x2 urgent/non-urgent tasks from the 
        tasks lists and populates the correct entries
        with them finally locking or 'seting' them until they are saved as 'done' 
        """
        
        self.suggest_non_urgent()
        self.suggest_urgent()
        self.suggest_project()

    def single_entry_empty(self, entry)->bool:
        """ takes a single entry(attr)obj name as an arg and,returns True if empty """
        contents = entry.get()
        print(f"Entry contents: {contents}")
        return bool(contents)
    
    def get_daily_tasks(self)->list:
        """ returns a list of entry content and a list of entry  names   """
        count = 0
        self.daily_tasks = []
        self.entry_names = []
        
        #get all entry content
        for entry in self.all_entries:
            count += 1
            if entry:
                content = entry.get()
                self.daily_tasks.append(content)
                self.entry_names.append(f"entry{count}")
        self.collected_content = [item for item in self.daily_tasks if item != ""]
        print(f"Collected daily tasks:{self.entry_names} ")#<- testing
        print(f"Collected daily tasks content:{self.collected_content} ")#<- testing
        
        #filter the list for empty strings
        return self.entry_names , self.collected_content
    
#TODO - write the below function save daily tasks
    def save_daily_tasks(self):

        if self.daily_tasks_set:
            
            all_entries_str = ["entry","entry2","entry3","entry4","entry5"]
            entry_content = []   
            entry_names = []

            #get set entry names
            for entry in all_entries_str:
                entry_attr = getattr(self, entry)
                if self.single_entry_empty(entry_attr):
                    entry_names.append(entry) #<- check for attribute or TKinter obj here

            #get all entry contente
            for entry in self.all_entries:
                content = entry.get()
                entry_content.append(content)
            print("Full entry_content:",entry_content)#<- testing
            
            #filter the list for empty strings
            filtered_entry_content = [item for item in entry_content if item != ""] 
            print("Filtered entry content to be saved",filtered_entry_content)#<- testing 

            #zip the list and cast the obj to a list 
            self.names_content_zipped = list(zip(entry_names, filtered_entry_content))

            # list comprehension to create a list of dictionaries to save for file persistance
            #save file should contain a dict daily_task_entry = {"entry_name":"entry2","content":"entry_text_here", "load_on_start":True}
            daily_tasks_to_save = [{"entry_name":tup[0],"content":tup[1], "load_on_start":True} for tup in self.names_content_zipped]
            print("Daily tasks to be saved:",daily_tasks_to_save)#<- testing

            save_file("daily_task_entry_lst.pkl", daily_tasks_to_save)


    def all_entries_empty(self)->bool:
        """ check all entries to see if they are empty, returns bool """
        
        #checks if all entries in list are truthy
        for entry in self.all_entries:
            if entry.get():  
                return False  #<-At least one entry is not empty
        
        #Else returns True
        return True  

    def if_required_load_file(self, file_path):
        """ checks whether the  "daily_task_entry.pkl" file needs to be loaded or not
        returns the contents of the bin file as a python var """

        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            if data.get("load_on_start", False): #<-second param here is default val
                    return data
            
            #print(f"File [{file_path}] not required load")

    def set_remedial_on_start(self):
        if self.all_entries_empty():
            pass
        else:
            for remedial_set_var in self.all_remedial_switch_vars:
                if remedial_set_var:
                    self.set_entries_callback()

    def set_entries_on_start(self):
        """ same as set entries but without the change of self.daily_tasks_set to True """
        print("set entries on start function ran()")#<- testing
        
        #check if all entries == empty they have entry configured to "set" the entry with text in 
        if self.all_entries_empty(): 
            pass

        else:
            for entry in self.all_entries:
                if entry.get():
                    entry.configure(state="disabled", border_width=3)
            self.toggle_set_entry_var()

    def set_entries_callback(self):
        """ locks all the entries in the 'todays tasks' frame and thickens the borders.
          IF they have text in. Also calls to toggle the Boolvars for the entries to show they are set"""
        print("set entries function ran()")#<- testing
        
        #check if all entries == empty they have entry configured to "set" the entry with text in 
        if self.all_entries_empty(): 
            pass

        else:
            self.daily_tasks_set = True
            for entry in self.all_entries:
                if entry.get():
                    entry.configure(state="disabled", border_width=3)
            print("toggle_set_entry_var ran()")
            self.toggle_set_entry_var()


    def toggle_set_entry_var(self):
        """ 
        toggles the entries BoolVar to show that entry has been set,
        called on set and clear. Only toggles the BoolVar if not empty 
        and not already set 
        """

        zipped = zip(self.all_entries, self.all_set_entry_vars)

        for entry, set_entry_var in zipped:
            if entry.get() and not set_entry_var.get(): 
                new_value = not set_entry_var.get()
                set_entry_var.set(new_value)
                print(f"{set_entry_var} set to = {new_value}")
            

    def sort_all_tasks(self):
        """ sorts all tasks using the sorting methods from 'algo.py' """
        algo()


    #suggest tasks function
    def get_top_tasks(self, class_inst, num_tasks)-> str: #list[str]
        """ 
        get text from task list text box and split on new line. 
        Takes task list class instance and number of lines of text as args, returns a list of strings 
        """
        #get text
        text = class_inst.textbox.get("1.0", "end-1c")
        #print(f"Text collected from Task List:{text}") #<- testing

        #split on new line
        split_text = text.splitlines() 
        #print(split_text)
        
        #slice to retun that number of elements
        return split_text[:num_tasks] 
    
 
    def clear_entries(self):
        """ clear all entries """

        entries = [self.entry, self.entry2, self.entry3, self.entry4, self.entry5]

        #delete the contents of all entreis in the entry widget list
        for entry in entries:
            entry.delete(0, "end")
        
    def reset_entries(self):
        """ re-configure entries to 'un-set' """

        self.entry.configure(state="normal", border_width=1, border_color="green")
        self.entry2.configure(state="normal", border_width=1, border_color="red")
        self.entry3.configure(state="normal", border_width=1, border_color="red")
        self.entry4.configure(state="normal", border_width=1, border_color="grey")
        self.entry5.configure(state="normal", border_width=1, border_color="grey")  

    def reset_clear(self):
        """ temp function to clear and reset entries """
        self.reset_entries()
        self.clear_entries()

    def insert_tasks(self, strings, entries) -> None:
        """ 
        Takes entry text to insert as a list of strings and a list of entries to insert them into in the same format.
        
        Arguments:
        strings -> ["name_of_entry_here", "name_of_entry2_here"] type -> lst(str)
        entries -> ["entry text here", "more entry text here"] type -> lst(str)

        Note: entries Type(str) used for easy file persistence 
        """
        for entry_name, string in zip(entries, strings):
            entry_attr = getattr(self, entry_name)
            entry_attr.delete(0, "end")
            entry_attr.insert(0, string)
        
    def unset_unlock(self, entry):
        """ Takes an entry obj as an arg and unlocks that entry, toggling the corresponding set boolvar """

        if entry in self.entry_var_dict:
            entry.configure(state="normal", border_width=1)
            bool_var = self.entry_var_dict[entry]

            bool_var.set(not bool_var.get())
            ###HERE

            print(f"Toggled [{self.get_entry_name(entry)}] bool var now set to:", bool_var.get())
        else:
            print("Error: Entry not in entry_var_dict, therefore, doesn't exist or cannot be set")

        






#Monthly focus
class MyFrame3(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height
        self.grid_rowconfigure(10, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)


        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=10)
        
        #remaining days label
        self.label2 = ctk.CTkLabel(self,anchor=ctk.S, text="Remaing days untill reset",width=60, height=60)
        self.label2.place(x=80,y=200)

        #number of days
        self.label3 = ctk.CTkLabel(self,anchor=ctk.S, text="6",width=60, height=60)
        self.label3.place(x=300,y=200)

        #custom clickable link class from tkinter
        self.label_text = 'Click here to see Trello "focus" board'
        self.link = "https://trello.com/b/EVzPMpFs/focus-by-calander"
        self.clickable_label = ClickableLinkLabel(self, text=self.label_text, link=self.link) #<- implemented own widget class based on tkinter
        self.clickable_label.place(x=20, y=50)

        # Testing remove once completed
        class_def.task_tracking.create_task("Project2", "testing projects", 8, 8, "testing","10-10-2025",isproject=True,isparent=True)

        #Combobox select a project 
        self.dropdown_options = class_def.task_tracking.return_all_parent_project_names()
        self.dropdown_options.insert(0,"Select a project")
        self.dropdown = ctk.CTkComboBox(self, values=self.dropdown_options,command=None, width=220)
        self.dropdown.set("Select a project")
        self.dropdown.place(x=50, y=90)
            
        # Bind the event to the update function this didnt work so well was meant to update the combobox options with projects on focus or hover but continually kep redrawing and was a nightmare so for prototype swtiched to button
        #self.dropdown.bind("<FocusIn>",self.update_combobox_options)

        #Entries
        self.entry_focus1 = ctk.CTkEntry(self,placeholder_text="Month Focus1",width=220)
        self.entry_focus1.place(x=50 , y=140)

        self.entry_focus2= ctk.CTkEntry(self,placeholder_text="Month Focus2",width=220)
        self.entry_focus2.place(x=50 , y=180)

        #Buttons
        self.button = ctk.CTkButton(self, text="Set focus",command=self.set_month_focus, height=28, width=28 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button.place(x=290,y=180)
        
        # Testing remove once completed
        self.button = ctk.CTkButton(self, text="testing\ntoggle set",command=self.toggle_set, height=28, width=28 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button.place(x=320, y=10)

        #update projects combobox
        self.button_update_dropdown = ctk.CTkButton(self, text="Update \n project list",fg_color="light blue",command=self.update_combobox_options, height=28, width=30 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button_update_dropdown.place(x=290, y=90)
        

        ################# on-start logic ######################
        self.set = None

        # Call the function and get the remaining days
        self.remaining_days = self.get_remaining_days_of_month()

        #TODO - if remaining days = 0 on load then reset entries

        print("Remaining days of the month:", self.remaining_days)

        #set the remaining_days to label
        self.label3.configure(text=self.remaining_days)

        #Load the month focus on start
        self.load_month_focus()

        #set the 'set' attribute
        self.set = load_file("focus_set.pkl")
        self.toggle_set(self.set)



################ methods ######################

    #TODO - reset month focus entries.
    #TODO - doc strings for all these functions
        
    def toggle_set(self, force_bool=None):
       """Toggles the bools var and takes an optional second bool parameter
          of True or False to force the toggle on or off; else, it will just toggle 
          the opposite of what it already is."""
    
       if force_bool is not None:
           self.set = force_bool
       else:
           self.set = not self.set

       if self.set:
           self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
           self.entry_focus2.configure(state="disabled", border_width=3, border_color="black")
           self.dropdown.configure(state="disabled", border_width=3, border_color="black")
       else:
           self.entry_focus1.configure(state="normal", border_width=1)
           self.entry_focus2.configure(state="normal", border_width=1)
           self.dropdown.configure(state="normal", border_width=1)


    def set_month_focus(self):

        if self.remaining_days == 0 or not self.set:
            #Get content of entries
            self.focus1 = self.entry_focus1.get()
            self.focus2 = self.entry_focus2.get()
            
            #'set' the entries
            self.toggle_set(True)
           
            #save the files
            save_file("focus1.pkl", self.focus1)
            save_file("focus2.pkl", self.focus2)
            save_file("focus_set.pkl",self.set)

        else:
            print("Please wait the remaining days until reset to set a new focus")
    
    def load_month_focus(self):
        self.focus1 = load_file("focus1.pkl")
        self.focus2 = load_file("focus2.pkl")

        self.entry_focus1.insert(0,self.focus1)
        self.entry_focus2.insert(0,self.focus2)

        if not self.set or self.remaining_days != 0:
            self.toggle_set(False)
        else:
            self.toggle_set(True)


    def get_remaining_days_of_month(self):
        #Get the current time in seconds since the epoch
        self.current_time = time.time()

        #Get the current time in a structured time format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        self.current_struct_time = time.localtime(self.current_time)

        #Calculate the last day of the month
        _, self.last_day = calendar.monthrange(self.current_struct_time.tm_year, self.current_struct_time.tm_mon) # month range returns tuple of day of the week (mon0-sun6) which the month starts and the secon val is the number of day month

        #Step 4: Calculate the remaining days
        self.remaining_days = self.last_day - self.current_struct_time.tm_mday # struct time obj can access each elem using the ".tm_xxx" tag

        return self.remaining_days
    
    #TODO - copied function from my fram for make the one in myframe for more universal and replace use "dropdownnamevarnamehere = self.dropdown["values"] = updated option"
    #note to self with the below function that there is the verion of the widget in the class and then the version in the app instance.
    #so the one in the class is the one first shown and then we destory it and create a new one in the app instance with the updated version
    #note add "event" as arg to this function to go back to binding other triggers
   
    def update_combobox_options(self):
        updated_options = class_def.task_tracking.return_all_parent_project_names()
        updated_options.insert(0, "None")
    
        # Destroy the existing ComboBox widget
        app.my_frame3.dropdown.destroy()
    
        # Recreate the ComboBox with the updated options
        app.my_frame3.dropdown = ctk.CTkComboBox(app.my_frame3, values=updated_options, width=220)
        app.my_frame3.dropdown.set("Select a project")
        app.my_frame3.dropdown.place(x=50, y=90)

        app.my_frame3.dropdown.bind("<FocusIn>",self.update_combobox_options)

    
        print("Successfully updated the combobox options:", updated_options)


    

################ methods2 ######################
        # TODO - use these methods to clear up the mega long lamda functions in the button widgets !!
    def suggest_non_urgent(self):
        """ takes the top two tasks from the non-urgent task list and puts them into the entries """
        #######testing insert_tasks
        self.insert_tasks(self.top_tasks,(self.entry4,self.entry5) )

    def suggest_todays_tasks(self): # split into sub-functions
        """ Takes x1 project and x2 urgent/non-urgent tasks from the tasks lists and populates the correct entries with them finally locking or 'seting' them until they are saved as 'done' """

    def set_todays_task(self):
        """ locks all the entries in the 'todays tasks' fram and thickens the borders """

    def sort_all_tasks(self):
        """ sorts all tasks using the sorting methods from 'algo.py' """
        algo()




    # need to add some function here to check if yesterdays tasks where done ? I think sorting should take car.

    # def insert_tasks(self, strings, *insert_entries):
    #     """ 
    #     Takes a single string or list of strings and the entries to populate as arguments.
    #     Deletes the current text and inserts the elements (str) into the insert_entries.
    #     Note: If multiple entries are passed to insert, type=tuple.
    #     """
    #     # Convert strings to a list of strings if it's a single string
    #     if isinstance(strings, str):
    #         strings = [strings]

    #     # Delete the current text #<-might not be needed
    #     for self.entry in insert_entries:
    #         self.entry.delete(0, "end")

    #     # Insert the strings into the insert_entries at the beginning
    #     for args in strings:
    #         for self.entry in insert_entries:
    #             self.entry.insert(0, args)
        

#Task manager
class MyFrame4(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # configure grid system
        self.grid_rowconfigure(8) 
        self.grid_columnconfigure(2)
    
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #testing task creation and setting (prior to setting display task) 
        # TODO - create two new tasks (factory and callbacks later for this)
        class_def.task_tracking.create_task("washing", "do the washing", 8, 4, "household","20-11-88")
        class_def.task_tracking.create_task("cleaning", "clean the house", 6, 2, "household","20-11-88")
        class_def.task_tracking.create_task("Project1", "testing projects", 8, 8, "testing","10-10-2025",isproject=True,isparent=True)
        

        # washing = class_def.task_tracking.get_task("washing")
        # class_def.task_tracking.set_display_task(washing)
        # display = class_def.task_tracking.get_display_task()
        # print(display)

        #Textbox single task
        self.textbox = ctk.CTkTextbox(self, width=300,height=310, corner_radius=3 ) 
        self.textbox.insert("0.0", "Task Display Window")
        self.textbox.insert("2.0", class_def.task_tracking.display_task)
        self.textbox.place(x=10, y=25)
        
        #Textbox all tasks
        self.textbox2 = ctk.CTkTextbox(self, width=300,height=310, corner_radius=3 ) 
        self.textbox2.insert("0.0", "All Tasks Display Window")


        #Buttons
        self.button_create_new_task = ctk.CTkButton(self, text="Create new task",command=self.create_task, height=28, width=45 ) 
        self.button_create_new_task.place(x=330, y=235)

        self.button_update_selected_task = ctk.CTkButton(self, text="Update selected task",command=self.update_selected_task, height=28, width=45 ) 
        self.button_update_selected_task.place(x=330, y=270)

        self.button_archive_task = ctk.CTkButton(self, text="Delete selected task",command=self.delete_selected_task ,height=28, width=45 ) 
        self.button_archive_task.place(x=330, y=305)

        self.button_clear_entries = ctk.CTkButton(self, text="Clear",fg_color="light blue",command=self.clear_entries, height=28, width=28 ) 
        self.button_clear_entries.place(x=468, y=270)

        self.button_select_task = ctk.CTkButton(self , text="Select Task", fg_color="dark blue", command=self.select_task,height=28, width=20 ) 
        self.button_select_task.place(x=440, y=235)


        self.button_update_dropdown = ctk.CTkButton(self, text="Update project list",fg_color="light blue",command=self.update_combobox_options, height=28, width=30 )
        self.button_update_dropdown.place(x=10, y=410)


        # switch
        self.switch_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(self,variable=self.switch_var,command=self.toggle_single_all_task_view,text=None, onvalue=True, offvalue=False)
        self.switch.place(x=330, y=340)

        #label for switch
        self.switch_label = ctk.CTkLabel(self,font=("",9) , text="View selected task/\nView all tasks",width=50 , height=10)
        self.switch_label.place_configure(x=370, y=340)
        self.switch_label.place()

        #Combobox
        self.dropdown_options = class_def.task_tracking.return_all_parent_project_names()
        print("self.dropdown_options",self.dropdown_options)
        self.dropdown_options.insert(-1, "None")
        self.dropdown_parent_project = ctk.CTkComboBox(self, width=350, values=self.dropdown_options, command=None)
        self.dropdown_parent_project.set("None")
        #postion self.dropdown_parent_project.place(x=140, y=380)

        #label for combobox
        self.dropdown_options_label = ctk.CTkLabel(self,text="Select a parent project and for new parent projects select 'None'" )

    
        

        #Entries
        self.entry_task_name = ctk.CTkEntry(self,placeholder_text="Task name", width=180)
        self.entry_task_name.place(x=330,y=25)
        
        #add an event listner for the enter button to select the task in the entry
        self.entry_task_name.bind("<Return>",self.select_task)

        #add an event listern for ctr + d and delete 
        self.entry_task_name.bind("<Control-d>",self.delete_selected_task)


        #add an event listener for ctrl + u to update
        self.entry_task_name.bind("<Control-u>",self.update_selected_task)



        self.entry_task_description = ctk.CTkEntry(self,placeholder_text="Task description", width=180)
        self.entry_task_description.place(x=330,y=60) 

        self.entry_task_urgency = ctk.CTkEntry(self,placeholder_text="Task urgency", width=180)
        self.entry_task_urgency.place(x=330,y=95) 
        
        self.entry_task_importance = ctk.CTkEntry(self,placeholder_text="Task importance", width=180)
        self.entry_task_importance.place(x=330,y=130) 
        
        self.entry_task_catagory = ctk.CTkEntry(self,placeholder_text="Task catagory", width=180)
        self.entry_task_catagory.place(x=330,y=165) 
        
        self.entry_task_due_date = ctk.CTkEntry(self,placeholder_text="Due date", width=180)
        self.entry_task_due_date.place(x=330,y=200) 


        self.all_entries = [
            self.entry_task_name,
            self.entry_task_description,
            self.entry_task_urgency,
            self.entry_task_importance,
            self.entry_task_catagory,
            self.entry_task_due_date
            ]
        

        #checkbox
        self.isproject_check_var = ctk.BooleanVar(value=False)  #change the name of this to is_project_check_var
        self.check = ctk.CTkCheckBox(self, text="Is a project", variable=self.isproject_check_var,command=lambda event=None: self.is_project_toggle(event), onvalue=True, offvalue=False) #"command=checkbox_event," needs to be added to the end 
        self.check.place(x=10,y=380)
        
        # bind the function on button release aswell
        self.check.bind("<Button-1>", self.is_project_toggle)

        #Button

        # Bind the event to the update function
        #self.check.bind("<Button-1>", self.update_combobox_options)

        



        #TODO - checkbox for prject selction to be shown on check line 617
        #TODO - add another check button for "is urgrent", possibly requires new attribute or setting task urgency attribute to 10
        #TODO - hide combo box until "project" checkbox checked then show list of projects
        
        ########## on start-up logic ###########
        
        #get and format task names into strings for all tasks to be displayed
        # self.textbox2.insert("2.0", "\n")
        # self.tasks = class_def.task_tracking.string_list_all_tasks() 
        # self.formatted_tasks = "\n".join([f"- {task}" for task in self.tasks])
        # for task in self.formatted_tasks:
        #     self.textbox2.insert("end",task )
        
        #keep running updates for changes made during runtime
        self.update_textbox2()


    ####### methods ###########

    def clear_entries(self):
        """ clear all entries """

        #delete the contents of all entreis in the entry widget list
        for entry in self.all_entries:
            entry.delete(0, "end")

    def update_combobox_options(self):
        """ update the list of options based on the project tasks in memorey """
        print("test")

        self.updated_options = class_def.task_tracking.return_all_parent_project_names()
        print("updated_options",self.updated_options)
        self.updated_options.insert(-1, "None")

        #update values
        self.dropdown_parent_project.destroy()

        # redraw the combobox
        if self.isproject_check_var:
            self.dropdown_parent_project = ctk.CTkComboBox(self, width=350, values=self.updated_options, command=None)
            self.dropdown_parent_project.set("None")
            self.dropdown_parent_project.place(x=140, y=380)


    def update_textbox(self):
        self.textbox.delete("2.0", "end")
        self.textbox.insert("2.0", class_def.task_tracking.display_task)



    # TODO - stop this from running every second and just update after you change the text using callback
    def update_textbox2(self):
        self.textbox2.delete("2.0", "end") #"2.0" = "line2.charachter 0"
        self.textbox2.insert("2.0", "\n")
        self.tasks = class_def.task_tracking.string_list_all_tasks() 
        self.formatted_tasks = "\n".join([f"- {task}" for task in self.tasks])
        
        for task in self.formatted_tasks:
            self.textbox2.insert("end",task )        
        
        # Schedule the function to run again after a specific time (in milliseconds)
        self.after(1000, self.update_textbox2)  # 1000 milliseconds = 1 second


    def toggle_single_all_task_view(self):

        self.switch_state = self.switch_var.get()
        print("toggle single all task view switch state:", self.switch_state)

        if self.switch_state:
            self.textbox2.place(x=10, y=35)
            self.textbox.place_forget()
        else:
            self.textbox.place(x=10,y=35)
            self.textbox2.place_forget()
    
    def is_project_toggle(self, event):

        self.check_var_state = self.isproject_check_var.get()
        print("toggle is project state:changed") 

        if self.check_var_state == True :
            self.dropdown_parent_project.place(x=140, y=380)
            self.dropdown_options_label.place(x=140, y=410)

            
        else:
            self.dropdown_parent_project.place_forget()
            self.dropdown_options_label.place_forget()
    
    def get_isparent(self)->bool:
        return self.dropdown_parent_project != "None"
    # TODO - needs error handling

    def get_all_entries(self):
        """ return the contents of all entries as a dict  """
        all_entries = {}

        all_entries['name'] = self.task_name = self.entry_task_name.get()
        all_entries['description'] = self.task_description = self.entry_task_description.get()
        all_entries['urgency'] = self.task_urgency = self.entry_task_urgency.get()
        all_entries['importance'] = self.task_importance = self.entry_task_importance.get()
        all_entries['catagory'] = self.task_catagory = self.entry_task_catagory.get()
        all_entries['due_date'] = self.task_due_date = self.entry_task_due_date.get()
        all_entries['isproject'] = self.isproject = self.isproject_check_var.get()
        all_entries['isparent'] = self.isparent = self.get_isparent()

        return all_entries

    
    def create_task(self):
        """ Collect all entry data and create a task instance  """
        
        self.task_name = self.entry_task_name.get()
        self.task_description = self.entry_task_description.get()
        self.task_urgency = self.entry_task_urgency.get()
        self.task_importance = self.entry_task_importance.get()
        self.task_catagory = self.entry_task_catagory.get()
        self.task_due_date = self.entry_task_due_date.get()
        self.isproject = self.isproject_check_var.get()
        self.isparent = self.get_isparent()

        #TODO - update the above so that I can use the get all entries method instead
        # TODO - add constraints and error handling for task creation here
        #date format YY-MM-DD (string)


        class_def.task_tracking.create_task(
            self.task_name,
            self.task_description,
            int(self.task_urgency),
            int(self.task_importance),
            self.task_catagory,
            self.task_due_date,
            self.isproject,
            self.isparent
            )
        
        #prints name of task and list of all tasks for testing
        print(f"Task {self.task_name} created")
        class_def.task_tracking.string_list_all_tasks()

    def update_selected_task(self, event=None):
        """ takes the task name as a string and any attributes to update """
        #TODO - currently this will update any task using the task name as a string I should update this so its only the currently selected task
        print("update_selected_task() was called")#<-testing
       
        #get the new entry conents
        entry_contents = self.get_all_entries() 
        print("entry_contents",entry_contents)#<-testing

        #get the task instance
        task_inst = class_def.task_tracking.get_task(entry_contents['name'])# THINK THIS MIGHT BE THE PROBLEM

        print(f"Before update - Task ID: {task_inst.id_}")
        print(f"Selected task to update [{task_inst.name}]")



        #compare the values and create a dict of the difference
        self.difference = {}

        for key, value in entry_contents.items(): #<- note to self dict methods - .items (all), .keys (keys), .values(values)
            if (key, value) not in vars(task_inst).items():
                self.difference.update({key: value})
        
        print("self.difference:",self.difference)#<- testing

        #update the different values
        task_inst.update_attributes(**self.difference)

        #print the updated instance attr
        print(f"task instance [{task_inst.name}] has been updated: {task_inst.__str__()}")

        #set the updated task to the display
        class_def.task_tracking.set_display_task(task_inst)

        #checking the task has been updated
        updated_display_task = class_def.task_tracking.get_display_task()

        print ("updated display task:", updated_display_task)

        print(f"Before after - Task ID: {task_inst.id_}")

        #updated the textbox
        self.update_textbox()

    def delete_selected_task(self, event=None):
        """ callback function for the delete button"""

        #get the selected task name
        selected_task = class_def.task_tracking.get_display_task()

        print("stack",class_def.task_tracking.task_archive.stack) #this seems to work but after running the rest of the method this stack is empty

        #add task to the archive stack and remove from task_tracking.all_tasks and all_stacks
        class_def.task_tracking.task_archive.archive_task(selected_task)

        #empty the display_task
        class_def.task_tracking.set_display_task('')

        #update both textboxes
        self.update_textbox()
        self.update_textbox2()

        #check the contents of the task stack
        print(f"names of tasks in 'task_archive':{class_def.task_tracking.task_archive.print_task_stack()}")
        print("deletion finished")


    def select_task(self, event=None):
        self.task_name = self.entry_task_name.get()
        print("test point 1") #testing
        print(f"self.task_name = {self.task_name}") #testing
        print(f"self.task_name type = {type(self.task_name)}")
        if not self.task_name:
            print("Please enter the name of the task you wish to view in the 'task_name' entry")
        
        self.selected_task = class_def.task_tracking.get_task(self.task_name)
        print(f"self.selected_task = {self.selected_task}") #testing

        if not self.selected_task:
            print("No tasks match that name please enter the exact name of the task")

        else: class_def.task_tracking.set_display_task(self.selected_task)
        print("Testing display task",class_def.task_tracking.get_display_task())
        self.update_textbox()

            

    


            
        
#Non urgent Task List
class MyFrame5(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # configure grid system
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(1, weight=1)
        
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Textbox
        self.textbox = ctk.CTkTextbox(self,height=500, width=250, corner_radius=3, text_color="blue" )
        self.textbox.grid(row=0, column=0)
        #self.textbox.insert("0.0", "Some example text!\n" * 50) #
        #self.textbox.configure(state="disable")
        
        ########## on-start control logic #########
        
        self.populate_task_list(class_def.task_tracking.non_urgent_task_stack)
        # testing to show whats in the stack
        class_def.task_tracking.non_urgent_task_stack.print_task_stack()

        #update list after every 1000 milliseconds (1s)
        #self.after(1000,lambda:self.populate_task_list(class_def.task_tracking.non_urgent_task_stack))

################ methods ######################
    def populate_task_list(self, task_stack):
        """ populates the task list with all relevant, takes the task_stack(obj) as arg """

    # Insert task names
        print("task_stack type:", type(task_stack))
        print("TESTING WORKING")
        task_stack.print_task_stack()
        task_names = task_stack.return_stack_names()
        print("task_names:",task_names)

        if task_names:
            print("inside populate task list for loop")
            self.textbox.configure(state="normal")
            self.textbox.delete("1.0", "end")
            for task_name in task_names:
                self.textbox.insert("end",f"{task_name}\n")
            #self.textbox.configure(state="disabled")
            print("Tasks text successfully inserted")
        else:
            # Insert alt text into box
            print("inside populate task list else block")
            self.textbox.insert("0.0", "Task list is empty. No tasks to display.")
            self.textbox.configure(state="disabled")
        



#Project Task List
class MyFrame5V2(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        #configure grid system
        self.grid_rowconfigure(20, weight=1) 
        self.grid_columnconfigure(1, weight=1)

        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0)


        #Textbox
        self.textbox = ctk.CTkTextbox(self,height=500, width=250, corner_radius=3, text_color="green" )
        self.textbox.grid(row=0, column=0)

        ############## on-start control logic ################
        self.populate_task_list()
    
################ methods ######################
# TODO - clean up the duplication here with the poulation of lists, try either a global function in utils or call the one from Myframe 5 and pass the textbox to populate as an arg rember to pass the instance of this class
    def populate_task_list(self):
        """ populates the task list with all the project tasks. """
        this_months_project = self.get_project_set_for_this_month()

    
        #checks if any project set this month
        if this_months_project:
            task_names = this_months_project.return_stack_names()
            for task_name in task_names:
                self.textbox.insert("end", task_name, "\n")
                self.textbox.configure(state="disabled")
                print("Project tasks text successfully inserted")
        else:
            #insert alt text into box
            self.textbox.insert("0.0", "To display project tasks please select a \n project for this month")
            self.textbox.configure(state="disabled")

    def get_project_set_for_this_month(self):
        """ gets the project set for this month, if none set returns none """
        project_task_list = class_def.task_tracking.project_stack.return_task_stack()
        for project in project_task_list:
            if project.set_for_this_month :
                return project
        return None


    # TODO -  mote to task manager frame
    # def switch_callback(self):
    #     print("switch swtiched!")


#Urgent Task List
class MyFrame5V3(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # configure grid system
        self.grid_rowconfigure(20, weight=1) 
        self.grid_columnconfigure(2, weight=1)
        
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Textbox
        self.textbox = ctk.CTkTextbox(self,height=500, width=250, corner_radius=3, fg_color="red") 
        self.textbox.grid(row=0, column=0)

        
        ########## on-start control logic #########
        MyFrame5.populate_task_list(self, class_def.task_tracking.urgent_stack)
        # testing to show whats in the stack
        class_def.task_tracking.urgent_stack.print_task_stack()


# #Task List parent frame example functions fune but : NOTE - that this messes with all the task sorting function namespace
# class MyFrame6(ctk.CTkFrame):
#     def __init__(self, master, title, width, height):
#         super().__init__(master, width, height)#<- calls the CTKframe for inheritance and we pass our width and hieght from the instantiation of this class to it

#         # Label
#         self.label = ctk.CTkLabel(self, text=title)
#         self.label.place(x=0, y=0)

#         # MyFrame5 instance
#         self.my_frame5 = MyFrame5(self, "Non Urgent Task List", 280, 550)
#         self.my_frame5.place(x=10,y=50)
        
## NOTE - change the instantiation of this class using the line below
#'self.my_frame5 = MyFrame6(self,"Non Urgent Task List",320, 650)'
        
#Additional info
class MyFrame6(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #gratitude
        #label
        self.gratitude_label = ctk.CTkLabel(self, text="5 Things you're thankful for")
        self.gratitude_label.place(x=20,y=25)

        #gratitide entries (x5)
        #used a dict of instances here incase names of the instances are needed.
        self.gratitude_entries_dict = {
            'gratitude_entry': ctk.CTkEntry(self, placeholder_text="Gratitude 1", width=220),
            'gratitude_entry2': ctk.CTkEntry(self, placeholder_text="Gratitude 2", width=220),
            'gratitude_entry3': ctk.CTkEntry(self, placeholder_text="Gratitude 3", width=220),
            'gratitude_entry4': ctk.CTkEntry(self, placeholder_text="Gratitude 4", width=220),
            'gratitude_entry5': ctk.CTkEntry(self, placeholder_text="Gratitude 5", width=220)
        }

        # Place the entries
        self.gratitude_entries_dict['gratitude_entry'].place(x=20, y=50)
        self.gratitude_entries_dict['gratitude_entry2'].place(x=20, y=85)
        self.gratitude_entries_dict['gratitude_entry3'].place(x=20, y=120)
        self.gratitude_entries_dict['gratitude_entry4'].place(x=20, y=155)
        self.gratitude_entries_dict['gratitude_entry5'].place(x=20, y=190)


        #Fitness label
        self.fitness_label = ctk.CTkLabel(self, text="Fitness")
        self.fitness_label.place(x=20,y=218)

        # Fitness entries
        self.fitness_entries_dict = {
            'fitness_entry1': ctk.CTkEntry(self, placeholder_text="Fitness 1", width=220),
            'fitness_entry2': ctk.CTkEntry(self, placeholder_text="Fitness 2", width=220)
        }

        # Place the fitness entries
        self.fitness_entries_dict['fitness_entry1'].place(x=20, y=240)
        self.fitness_entries_dict['fitness_entry2'].place(x=20, y=275)

        #how you feel 1-10 entry type(int)0-12 only
        self.how_you_feel_label = ctk.CTkLabel(self,text="How you feel?")
        self.how_you_feel_entry = ctk.CTkEntry(self,placeholder_text="1-10",width=40)

        #place how you feel widgets
        self.how_you_feel_label.place(x=20, y=308)
        self.how_you_feel_entry.place(x=20, y=333)

        #Notes textbox
        self.notes_textbox_label = ctk.CTkLabel(self, text="Notes")
        self.notes_textbox = ctk.CTkTextbox(self, width=290,height=310, corner_radius=3)

        #place Notes widgets
        self.notes_textbox_label.place(x=20, y=370)
        self.notes_textbox.place(x=20, y=400)

        #Desire label
        self.fitness_label = ctk.CTkLabel(self, text="What do you most desire?")
        self.fitness_label.place(x=20,y=720)

        #Desire entries dict
        self.desire_entries_dict = {
            'desire_entry': ctk.CTkEntry(self, placeholder_text="Desire 1", width=220),
            #'desire_entry2': ctk.CTkEntry(self, placeholder_text="Desire 2", width=220),
        }

        #Place the entries
        self.desire_entries_dict['desire_entry'].place(x=20, y=744)
        #self.desire_entries_dict['desire_entry2'].place(x=20, y=780)

         ######## on start logic ########
    
    #### methods ######





############################################ DEFINING APP CLASS ############################################

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1350x850")
        self.grid_rowconfigure(3)  # configure grid system
        self.grid_columnconfigure(2)

        #Habit Tasks Frame
        self.my_frame = MyFrame(self,"Habit Tasks", 50 , 30, self) # frame args order: width, height 
        self.my_frame.grid(row=0, column=0, padx=10, pady=10 )

        #Today's tasks Frame
        """ MyFrame2 Uses dependacy injection to share data  instance to another class. 
        essentially linking the two via pointing so I can get data from the instance of my_frame2 here in the App class """

        self.my_frame2 = MyFrame2(self, "Today's Tasks",520 ,260 ,self) #<- second self passes instance to 'app_instance' in MyFrame2 
        self.my_frame2.grid(row=0, column=1, padx=10, pady=10 )

        #Monthly Focus Frame
        self.my_frame3 = MyFrame3(self,"Monthly Focus",380, 250)
        self.my_frame3.grid(row=0, column=2, padx=10, pady=10 )

        #Task manager
        self.my_frame4 = MyFrame4(self,"Task Manager",515, 600)
        self.my_frame4.grid(row=1, column=0, padx=10, pady=10) 

        #Task list
        self.my_frame5 = MyFrame5(self,"Non Urgent Task List",280, 550)
        #self.my_frame5.grid(row=1, column=1, padx=2, pady=10) 
        self.my_frame5.place(x=580, y=380)

        #Project task list
        self.my_frame5v2 = MyFrame5V2(self,"Project Task List",280, 550)
        #self.my_frame5v2.grid(row=1, column=2, padx=2, pady=10) 
        self.my_frame5v2.place(x=900, y=380)

        #Urgent Task list
        self.my_frame5v3 = MyFrame5V3(self,"Urgent Task List",280, 550)
        #self.my_frame5v3.grid(row=1, column=3, padx=2, pady=10,)
        self.my_frame5v3.place(x=1200, y=380)

        #finish for the day button (remove once finished testing and save on close or similar)
        self.button_finish = ctk.CTkButton(self, text="Finish for the day \n Save All",command=self.finish_for_day, height=60, width=85 ) 
        self.button_finish.place(x=1650, y=40)

        #Additional info frame
        self.my_frame6 = MyFrame6(self,"Addtional info", 340, 825)
        self.my_frame6.place(x=1530, y=130)

        
    
    ########## methods  ##############
    def get_set_flags(self)->list:
        """ returns  one of the daily habits set flags
         and one of the daily tasks set flags type=lst(bool) """
        self.habit_set_flags = []
        self.daily_set_flags = []
        print("testing get_set_flags()")

        for habit_set_var in self.my_frame.all_habit_boolvars:
            value = habit_set_var.get()
            self.habit_set_flags.append(value)
        
        #this only does the daily task entries
        for set_var in self.my_frame2.all_set_entry_vars:
            new_value = set_var.get()
            self.daily_set_flags.append(new_value)

        #testing
        print(f"habit set flags:{self.habit_set_flags} daily_set_flags:{self.daily_set_flags}")

        #extend the habit_set_flags list in place 
        self.habit_set_flags.extend(self.daily_set_flags)

        return self.habit_set_flags 
    
    def get_daily_tasks_set_flags(self):
        """ returns a list of string type integers representing the boolean values
        of if the entries have been set or not
        returns: ('1','0','0','1','1')
        """
        #get the flags
        full_bool_list = self.get_set_flags()

        # Slice the first two elements with the string "1" or "0" conditions
        sliced_list = ["1" if val else "0" for val in full_bool_list[:2]]
        
        return sliced_list
        

    def get_done_flags(self, return_done_flags_and_entries_dict=False) -> list or dict:
        """ 
        Returns a list of all done_flags using BooleanVar.get() method
        if return_done_flags_and_entries_dict=True then a tuple is returned of
        done_flags and their correspoding entry so that the entries can be reset
        """
        #note - have to use ids as boovar objects are non hasshable so cant be used as dict keys (non unique)
        checkbox_vars = {
            "habit1": self.my_frame.entry_habit1,
            "habit2": self.my_frame.entry_habit2,
            "Project": self.my_frame2.entry,
            "urgent1": self.my_frame2.entry2,
            "urgent2": self.my_frame2.entry3,
            "non_urgent1": self.my_frame2.entry4,
            "non_urgent2": self.my_frame2.entry5
        }

        self.done_flags = [self.my_frame.habit1_check_var.get(),
                    self.my_frame.habit2_check_var2.get(),
                    self.my_frame2.project_check_var.get(),
                    self.my_frame2.urgent_check1_var.get(),
                    self.my_frame2.urgent_check2_var.get(),
                    self.my_frame2.non_urgent_check1_var.get(),
                    self.my_frame2.non_urgent_check2_var.get()]
        
        print("done_flags returned as list:", self.done_flags) # <- testing

        if return_done_flags_and_entries_dict:
            self.done_flags = tuple(zip(self.done_flags, checkbox_vars.values()))

            print("done_flags and entries returned as tuple:", self.done_flags)

        return self.done_flags
    
    def get_daily_tasks_done_flags(self):
        """ get the done flags and return them as integers representing boool vals for DB
        returns: ('1','0','0','1','1') 
        """
        done_flag_tuple = []
        
        self.done_flags = [self.my_frame.habit1_check_var.get(),
                    self.my_frame.habit2_check_var2.get(),
                    self.my_frame2.project_check_var.get(),
                    self.my_frame2.urgent_check1_var.get(),
                    self.my_frame2.urgent_check2_var.get(),
                    self.my_frame2.non_urgent_check1_var.get(),
                    self.my_frame2.non_urgent_check2_var.get()]
        
        for val in self.done_flags:
            if val:
                done_flag_tuple.append("1")
            else: 
                done_flag_tuple.append("0")
        
        return tuple(done_flag_tuple)

    
    def get_remedial_flags(self):
        """ 
        return the remeidal flags a list of bools 
        example:[True, False, False, False, False]
        """

        self.remedial_flags_dict =self.my_frame2.update_entries_dict()#<- CHECK WHAT THE CONTENTS OF THIS DICT LOOKS LIKE AND WRITE IT IN THE DOC STRING
        self.remedial_flags = list(self.remedial_flags_dict.values())
        print("remedial_flags",self.remedial_flags)
        
        return self.remedial_flags
    
    def get_remedial_set_flags(self):
        """ 
        retunrs a tuple of string type "1" or "0" for boolean values that
        indicate if the entries have been set into remedial mode .
        returns:('1','1','0','1','0')
        """
        remedial_list = [val.get() for val in app.my_frame2.all_remedial_switch_vars]

        # create list comp for returned tuple
        remedial_as_str_int = ["1" if x else "0" for x in remedial_list]

        return tuple(remedial_as_str_int)
    

    def get_original_content(self, from_button=False):
        """ 
        return the orignal content for the remedial tasks as lst(str)
        from_button is a bool passed to remedial_switch_capture to stop the
        unsetting of the entry  if called from button as opposed to switch 
        """

        #update the vars and switches dict
        self.original_content_dict = self.my_frame2.remedial_switch_capture(
        self.my_frame2.update_entries_dict(),from_button)
        self.original_content = list(self.original_content_dict.values())

        print("TESTING SELF.ORIGINAL_CONTENT",self.original_content)

        return self.original_content
    
    def if_done_checked_unlock_and_empty(self):
        """If done checked, unlock and empty entry"""
        done_flags = self.get_done_flags(return_done_flags_and_entries_dict=True)
        for done_flag , entry in done_flags:
            if done_flag and (entry not in(self.my_frame.entry_habit1,self.my_frame.entry_habit2)):
                entry.configure(state="normal", border_width=1)
                entry.delete(0, "end")

    
    #callback Finish for the day button
    def finish_for_day(self):
        """ callback function that gets all the required data to save """
        #get the data to pass to the DB in tuple(str,str) formatt
        ## daily habits VALUES
        daily_habits = self.my_frame.get_habits()#('habit1',)('habit2',)
        daily_set_duration = self.my_frame.get_set_duration_var() #('10',)
        daily_done_flags = self.my_frame.get_habit_done_flags() #('1','0')
        daily_set_on = (self.my_frame.get_habit_set_timestamp(),) # (Year-Month-Day Hour:Minute:Second) might need to remove the seconds
        daily_days_remaining = self.my_frame.get_days_remaining() #('3',)
        
        daily_habits_tuple = daily_habits + daily_set_duration + daily_done_flags + daily_set_on + daily_days_remaining 
        
        #debugging        
        print("daily_habits_tuple:",daily_habits_tuple)

        ## todays tasks
        todays_tasks_entries, todays_tasks_contents = self.my_frame2.get_daily_tasks() #('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
        done_flags = self.get_daily_tasks_done_flags() #('1','0','0','1','1')
        set_flags = self.get_daily_tasks_set_flags() #('0', '1', '0', '0', '1')
        remedial_set_flags = self.get_remedial_set_flag() #('0', '1', '0', '0', '1')
        remedial_contents = self.get_original_content(from_button=True)#('content1', 'content2', 'content3', 'content4', 'content5')

        #todays tasks tuple
        todays_tasks_tuple = todays_tasks_entries + todays_tasks_contents + done_flags + set_flags + remedial_set_flags + remedial_contents
        
        
        #print("duration_to_record",duration_to_record)
        #print("Set flags:",set_flags)

        #habit_names, habits =self.my_frame.get_habits_names()
        #task_names, tasks = self.my_frame2.get_daily_tasks()
        
        #record all frames
        frame_recorder = data_structure.RecordFrame()

        #daily habits
        frame_recorder.create_entry("daily_habits",daily_habits_tuple)
        print("daily_habits have been successfully recorded!") 

        #daily tasks
        frame_recorder.create_entry("todays_tasks",todays_tasks_tuple) 
        print("todays_tasks have been successfully recorded!") 


        # if done is checked empty and unlock the entry
        self.if_done_checked_unlock_and_empty()



                


#TODO - drop down menu for project tasks that shows tasks from that project in middle frame, project can only be selected if monthly focus aligns and once set cant be unset until....
#TODO - finish for the day button should be turned into a save progress, it also should have an entry below it that takes nots and feeling 1-10





 ############################################################################################       

if __name__ == "__main__":


    washing = None

    app = App()
    app.title("Tasker")

    #app.iconify()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()


