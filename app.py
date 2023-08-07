from class_def import *
import pickle
import customtkinter as ctk
import time
import calendar
from link_click import ClickableLinkLabel

########################################  UTILS #####################################
"""  persistance used to save load and update stored data on opening of app """

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

    # save duration on close
    app.my_frame.save_duration(app.my_frame.get_current_duration())
    
    app.destroy()  # Close the CTKinter app


#####################################################################################

###################### DEFINING FRAMES AND WIDGETS ###################################
#Habit Tasks
class MyFrame(ctk.CTkFrame):

    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # --Add widgets onto the frame--

        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Remaining days label
        self.label2 = ctk.CTkLabel(self,anchor=ctk.S, text="Remaing days untill end of habit forming",width=60, height=60)
        self.label2.grid(row=3, column=0, padx=10, pady=5)

        #Number of days label
        self.label_number_of_days_remaining = ctk.CTkLabel(self,anchor=ctk.S, text="loading duration...",width=60, height=60) 
        self.label_number_of_days_remaining.grid(row=3, column=2, padx=10, pady=5)

        #Entries
        self.entry_habit1 = ctk.CTkEntry(self,placeholder_text="Habit1",width=180)
        self.entry_habit1.grid(row=1, column=0, padx=10, pady=10)

        self.entry_habit2 = ctk.CTkEntry(self,placeholder_text="Habit2",width=180)
        self.entry_habit2.grid(row=2, column=0, padx=10, pady=10)

        self.entry_duration = ctk.CTkEntry(self, placeholder_text="Duration",width=70)
        self.entry_duration.grid(row=3, column=3, padx=10, pady=10)

        #Buttons
        self.button = ctk.CTkButton(self, text="set habits and duration",command=self.set_habits_and_duration ,height=28, width=28 ) 
        self.button.grid(row=1, column=3, padx=20)

        #TODO - remove once button placement is correct
        #self.button2 = ctk.CTkButton(self, text="set duration",command=self.xxxxxx, height=28, width=28 ) 
        #self.button2.grid(row=2, column=3, padx=20)

        #Checkboxes
        check_var = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check = ctk.CTkCheckBox(self, text="Done", variable=check_var, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check.grid(row=1, column=2)

        check_var2 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check2 = ctk.CTkCheckBox(self, text="Done", variable=check_var2, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check2.grid(row=2, column=2)

        #TODO - remove - Load the habits
        #self.habit1 =load_file("habit1.pkl")
        #self.habit2 = load_file("habit2.pkl")

        # configure grid system
        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(2, weight=1)

        ############## on-start control logic ################
        # TODO

        ##duration
        #load duration
        self.loaded_duration = self.load_duration() 
        print(self.loaded_duration)
        #updates the duration based on elapsed time then schedules next update for 24hrs
        self.update_duration(self.loaded_duration)

        #gets the duration and saves it locally
        self.save_duration(self.get_current_duration())

        # on-close function edited for save duration for file persistance 
        
        ## habits
        #load the habit files as a tuple
        self.loaded_habits = self.load_habits()

        # re-set the entries or load the loaded vals into the habit1/2 entries.
        if self.loaded_duration == 0:
            self.reset_habits()
        else:
            self.set_habits(self.loaded_habits)

        # on-close function edited to save habits for file persistance 
        ##

    
    
    ############## methods ##############

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
        self.entry_habit1.delete(0,"end") #<- TODO check "end" syntax works instead of 999
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
        print (f"habit duration set to:{duration_to_set}")

    def get_entry_duration(self)->str:
        """ gets whatever is in the 'duration' entry, returns it as an str """
        self.duration = self.entry_duration.get()
        return self.duration            
    
    def get_current_duration(self)-> int:
        """ gets whatever is currently set as the remaining days label and returns it an int. """
        current_duration = self.label_number_of_days_remaining.cget("text")
        return int(current_duration)
    
    def schedule_update(self, duration_hours, function):
        """Schedule the passed function  to run after the specified number of hours."""
        milliseconds = duration_hours * 60 * 60 * 1000
        self.after(milliseconds, function)

    def update_duration(self, loaded_duration):
        """takes the loaded duration as an arg(int)
        updates the duration using the elapsed days and set duration functions,
        finally scheduling the next update for 24 hours time """

        # Update the duration based on elapsed days
        self.whole_elapsed_days = self.get_elapsed_days()
        print("Number of days to deduct from duration:",self.whole_elapsed_days)

        # set updated duration
        print("Current loaded duration:", loaded_duration)
        if loaded_duration <= 0: #<- should account for accidental minus durations (shouldnt occur anyway)
            self.set_duration(0)
        else:
            self.updated_duration = loaded_duration - self.whole_elapsed_days
            self.set_duration(self.updated_duration)

        # Schedule next update
        self.schedule_update(24, self.update_duration)

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
        print(type(self.elapse))
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


#Todays Tasks
class MyFrame2(ctk.CTkFrame):
    def __init__(self, master,text, width, height, app_instance):
        super().__init__(master, width, height)

        # reference to the App instance for later use
        self.app_instance = app_instance

        #Set the title and frame size on instantiation
        self.val = text
        self.val2 = width
        self.val3 = height

        self.grid_rowconfigure(10, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)

        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        #Entries
        self.entry = ctk.CTkEntry(self,placeholder_text="Project", border_color="green",text_color="green", border_width=3, width=180)
        self.entry.grid(row=0, column=0, padx=10, pady=10) 
 
        self.entry2 = ctk.CTkEntry(self,placeholder_text="Urgent",border_color="red",text_color="red", width=180)
        self.entry2.grid(row=1, column=0, padx=10, pady=10)    

        self.entry3 = ctk.CTkEntry(self,placeholder_text="Urgent",border_color="red",text_color="red" , width=180)
        self.entry3.grid(row=2, column=0, padx=10, pady=10) 
       
        self.entry4 = ctk.CTkEntry(self,placeholder_text="Task1",width=180)
        self.entry4.grid(row=3, column=0, padx=10, pady=10)

        self.entry5 = ctk.CTkEntry(self,placeholder_text="Task2",width=180)
        self.entry5.grid(row=4, column=0, padx=10, pady=10)    

        #Buttons
        self.button_suggest = ctk.CTkButton(self, text="suggest",command=self.suggest_non_urgent, height=28, width=28 ) 
        self.button_suggest.grid(row=0, column=3, padx=20)    

        self.button_set = ctk.CTkButton(self, text="set", height=28, width=50 ) 
        self.button_set.grid(row=2, column=3, padx=5)

        self.button_sort = ctk.CTkButton(self, text="sort all tasks", height=28, width=45 ) 
        self.button_sort.grid(row=1, column=3, padx=20)
        
        self.button_clear = ctk.CTkButton(self, text="clear all",command=self.clear_entries, height=28, width=45 ) 
        self.button_clear.grid(row=3, column=3, padx=20)


        #Checkboxes
        self.check_var = ctk.StringVar(value="off") #<- these should all be instance .self vars
        self.check = ctk.CTkCheckBox(self, text="Done", variable=self.check_var,border_color="green", onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check.grid(row=0, column=2)

        check_var1 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check1 = ctk.CTkCheckBox(self, text="Done", variable=check_var1, onvalue="on", border_color="red", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check1.grid(row=1, column=2)   

        check_var2 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check2 = ctk.CTkCheckBox(self, text="Done", variable=check_var2, onvalue="on",border_color="red", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check2.grid(row=2, column=2)   

        check_var3 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check3 = ctk.CTkCheckBox(self, text="Done", variable=check_var3, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check3.grid(row=3, column=2)   

        check_var4 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check4 = ctk.CTkCheckBox(self, text="Done", variable=check_var4, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check4.grid(row=4, column=2)    

        ############ on-start control logic ###########

################ methods ######################
    def suggest_non_urgent(self):
        """ takes the top two tasks from the non-urgent task list and puts them into the entries """

        #Access the instance from App class
        my_frame5_instance = self.app_instance.my_frame5
        
        #get the top 2 tasks from app.my_frame5 (Non-urgent task list)
        top_tasks = self.get_top_tasks(my_frame5_instance,2)
        print("top tasks:" ,top_tasks)

        #insert these tasks into the selected entries
        self.insert_tasks(top_tasks,(self.entry4, self.entry5)) # Non-urgent task entries



    def suggest_todays_tasks(self): # split into sub-functions
        """ Takes x1 project and x2 urgent/non-urgent tasks from the tasks lists and populates the correct entries with them finally locking or 'seting' them until they are saved as 'done' """

    def set_todays_task(self):
        """ locks all the entries in the 'todays tasks' fram and thickens the borders """

    def sort_all_tasks(self):
        """ sorts all tasks using the sorting methods from 'algo.py' """

    #suggest tasks function
    def get_top_tasks(self, class_inst, num_tasks)-> str: #list[str]
        """ 
        get text from task list text box and split on new line. 
        Takes task list class instance and number of lines of text as args, returns a list of strings 
        """
        #get text
        text = class_inst.textbox.get("1.0", "end-1c")#<- dont think -1 works here
        #print(f"Text collected from Task List:{text}") #<- testing

        #split on new line
        split_text = text.splitlines() 
        #print(split_text)
        
        #slice to retun that number of elements
        return split_text[:num_tasks] 
    
 
    def clear_entries(self):
        """ clear all entries """

        #create list of all entries using getattr (uses this syntax->"getattr(object, name[, default]") to get the values of an attribute)
        entry_widgets = [getattr(self, "entry")] + [getattr(self, f"entry{i}") for i in range(2, 6)]

        #delete the contents of all entreis in the entry widget list
        for entry_widget in entry_widgets:
            entry_widget.delete(0, "end")



 

    def insert_tasks(self, strings, insert_entries):
        """ 
        Takes a single string or list of strings and the entries to populate as arguments.
        Deletes the current text and inserts the elements (str) into the insert_entries.
        Note: If multiple entries are passed to insert, type=tuple.
        """
        # Convert strings to a list of strings if it's a single string
        if isinstance(strings, str):
            strings = [strings]

        # Delete the current text #<-might not be needed
        for entry in insert_entries:
            entry.delete(0, "end")

        # Use zip to pair each string with its corresponding entry, upacks from list of tuples  then inserts each string in an entry using the for loop
        for string, entry in zip(strings, insert_entries):
            entry.insert(0, string)


#Monthly focus
class MyFrame3(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height
        self.grid_rowconfigure(10, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)

        ### Add widgets onto the frame
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=10)
        
        #remaining days label
        self.label2 = ctk.CTkLabel(self,anchor=ctk.S, text="Remaing days untill reset",width=60, height=60)
        self.label2.grid(row=10, column=0, padx=1, pady=5)

        #number of days
        self.label3 = ctk.CTkLabel(self,anchor=ctk.S, text="6",width=60, height=60)
        self.label3.grid(row=10, column=3, padx=10, pady=5)

        #custom clickable link class from tkinter
        self.label_text = 'Click here to see Trello "focus" board'
        self.link = "https://trello.com/b/EVzPMpFs/focus-by-calander"
        self.clickable_label = ClickableLinkLabel(self, text=self.label_text, link=self.link) #<- implemented own widget class based on tkinter
        self.clickable_label.grid(row=0, column=0, padx=10, pady=20)

        # TODO - self population by listing all "projects" only availible when monthly focus "not-set"
        #Combobox
        self.dropdown = ctk.CTkComboBox(self,border_color="green", values=["Select a project","option 1", "option 2"],command=self.combobox_callback)
        self.dropdown.set("Select a project")
        self.dropdown.grid(row=1, column=0, padx=10, pady=5)

        #TODO - show option only on zero count something along the lines of:
        #if remain days == 0: combobox.pack/grid()

        #Entries
        self.entry_focus1 = ctk.CTkEntry(self,placeholder_text="Month Focus1",width=180)
        self.entry_focus1.grid(row=7, column=0, padx=10, pady=20)

        self.entry_focus2= ctk.CTkEntry(self,placeholder_text="Month Focus2",width=180)
        self.entry_focus2.grid(row=9, column=0, padx=10, pady=1)

        #Button
        self.button = ctk.CTkButton(self, text="Set focus",command=self.set_month_focus, height=28, width=28 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button.grid(row=9, column=3, padx=20)
        

        ################# on-start logic ######################

        # Call the function and get the remaining days
        self.remaining_days = self.get_remaining_days_of_month()

        #TODO - if remaining days = 0 on load then reset entries

        print("Remaining days of the month:", self.remaining_days)

        #set the remaining_days to label
        self.label3.configure(text=self.remaining_days)

        #Load the month focus on start
        self.load_month_focus()



################ methods ######################

    #TODO - reset month focus entries.
    #TODO - doc strings for all these functions

    def set_month_focus(self):
        if self.remaining_days == 0:
            #Get content of entries
            self.focus1 = self.entry_focus1.get()
            self.focus2 = self.entry_focus2.get()
            
            #'set' the entries
            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
           
            #save the files
            save_file("focus1.pkl", self.focus1)
            save_file("focus2.pkl", self.focus2)

        else:
            print("Please wait the remaining days until reset to set a new focus")
    
    def load_month_focus(self):
        self.focus1 = load_file("focus1.pkl")
        self.focus2 = load_file("focus2.pkl")

        self.entry_focus1.insert(0,self.focus1)
        self.entry_focus2.insert(0,self.focus2)

        if self.remaining_days != 0:
            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_focus2.configure(state="disabled", border_width=3, border_color="black")


    def get_remaining_days_of_month(self):
        #Get the current time in seconds since the epoch
        self.current_time = time.time()

        #Get the current time in a structured time format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        self.current_struct_time = time.localtime(self.current_time)

        #Calculate the last day of the month
        _, self.last_day = calendar.monthrange(self.current_struct_time.tm_year, self.current_struct_time.tm_mon) # month range returns tuple of day of the week (mon0-sun6) which the month starts and the secon val is the number of days in this month

        #Step 4: Calculate the remaining days
        self.remaining_days = self.last_day - self.current_struct_time.tm_mday # struct time obj can access each elem using the ".tm_xxx" tag

        return self.remaining_days
    
    def combobox_callback(self, choice):
        print("combobox dropdown clicked:", choice) #<- TODO

################ methods2 ######################
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




    # need to add some function here to check if yesterdays tasks where done ? I think sorting should take care of this.

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

        #Textbox
        self.textbox = ctk.CTkTextbox(self, width=300,height=310, corner_radius=3 ) # insert at line 0 character 0
        self.textbox.grid(row=0, column=0)
        self.textbox.insert("0.0", "Task Display Window")# <- need to finish this line
        self.textbox.insert("2.0",TaskTracking.display_task)# <- monitor when changing to class_def2

        #Buttons
        self.button_sort = ctk.CTkButton(self, text="View selected task", height=28, width=45 ) 
        self.button_sort.grid(row=0, column=2, padx=20,pady=20)

        self.button_sort = ctk.CTkButton(self, text="Edit selected task", height=28, width=45 ) 
        self.button_sort.grid(row=1, column=2, padx=20, pady=20)

        self.button_sort = ctk.CTkButton(self, text="Add new task", height=28, width=45 ) 
        self.button_sort.grid(row=2, column=2, padx=20,pady=20)

        #Entries
        self.entry = ctk.CTkEntry(self,placeholder_text="Task name", width=180)
        self.entry.grid(row=1, column=0, padx=10, pady=10) 

        self.entry = ctk.CTkEntry(self,placeholder_text="Task description", width=180)
        self.entry.grid(row=2, column=0, padx=10, pady=10) 

        self.entry = ctk.CTkEntry(self,placeholder_text="Task urgency", width=180)
        self.entry.grid(row=3, column=0, padx=10, pady=10) 

        self.entry = ctk.CTkEntry(self,placeholder_text="Task importance", width=180)
        self.entry.grid(row=4, column=0, padx=10, pady=10) 

        self.entry = ctk.CTkEntry(self,placeholder_text="Task catagory", width=180)
        self.entry.grid(row=5, column=0, padx=10, pady=10) 

        #checkbox
        check_var = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check = ctk.CTkCheckBox(self, text="Is a project", variable=check_var, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check.grid(row=6, column=0, padx=10, pady=10)
        

        #Combobox
        self.dropdown = ctk.CTkComboBox(self, values=["Select a project","option 1", "option 2"],command=None)
        self.dropdown.set("Select a project")
        self.dropdown.grid(row=6, column=1, padx=10, pady=5) #<- if is project checkbox checked this should be shown to select which task

        #TODO - checkbox for prject selction to be shown on check line 617
        #TODO - add another check button for "is urgrent", possibly requires new attribute or setting task urgency attribute to 10
        #TODO - hide combo box until "project" checkbox checked then show list of projects


#Task List
class MyFrame5(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # configure grid system
        self.grid_rowconfigure(20, weight=1) 
        self.grid_columnconfigure(3, weight=1)
        
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Textbox
        self.textbox = ctk.CTkTextbox(self,height=500, width=200, corner_radius=3 )
        self.textbox.grid(row=0, column=0)
        self.textbox.insert("0.0", "Some example text!\n" * 50) #
        self.textbox.configure(state="disabled")

################ methods ######################

    #method here to use a list to display the name attribute of the task objects, then join them all in one string with a new line for the textbox insertline 575

#Project Task List
class MyFrame5V2(ctk.CTkFrame):
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
        self.textbox = ctk.CTkTextbox(self,height=500, width=200, corner_radius=3, text_color="green" ) # insert at line 0 character 0
        self.textbox.grid(row=0, column=0)
        self.textbox.insert("0.0", "Some example text!\n" * 15)
        self.textbox.configure(state="disabled")


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
        self.textbox = ctk.CTkTextbox(self,height=500, width=200, corner_radius=3, fg_color="red") # insert at line 0 character 0
        self.textbox.grid(row=0, column=0)
        self.textbox.insert("0.0", "Some example text!\n" * 5)
        self.textbox.configure(state="disabled")


############################################ DEFINING APP CLASS ############################################

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1350x850")
        self.grid_rowconfigure(3)  # configure grid system
        self.grid_columnconfigure(2)

        #Habit Tasks Frame
        self.my_frame = MyFrame(self,"Habit Tasks", 50 , 30) # frame args order: width, height 
        self.my_frame.grid(row=0, column=0, padx=10, pady=10 )

        #Today's tasks Frame
        """ MyFrame2 Uses dependacy injection to share data from this instance to another class. 
        essentially linking the two via pointing so I can get data from the instance of my_frame2 here in the App class """

        self.my_frame2 = MyFrame2(self, "Today's Tasks", 200, 90,self) #<- second self passes instance to 'app_instance' in MyFrame2 
        self.my_frame2.grid(row=0, column=1, padx=10, pady=10 )

        #Monthly Focus Frame
        self.my_frame3 = MyFrame3(self,"Monthly Focus",300, 80)
        self.my_frame3.grid(row=0, column=2, padx=10, pady=10 )

        #Task manager
        self.my_frame4 = MyFrame4(self,"Task Manager",300, 350)
        self.my_frame4.grid(row=1, column=0, padx=10, pady=10) 

        #Task list
        self.my_frame5 = MyFrame5(self,"Task List",220, 550 )
        self.my_frame5.grid(row=1, column=1, padx=2, pady=10) 

        #Project task list
        self.my_frame5v2 = MyFrame5V2(self,"Project Task List",220, 550 )
        self.my_frame5v2.grid(row=1, column=2, padx=2, pady=10) 

        #Urgent Task list
        self.my_frame5v3 = MyFrame5V3(self,"Urgent/Admin Task List",220, 550 )
        self.my_frame5v3.grid(row=1, column=3, padx=2, pady=10,)



        self.button_finish = ctk.CTkButton(self, text="Finish for the day \n Save All",command=self.button_event, height=60, width=85 ) 
        self.button_finish.grid(row=0, column=3, padx=20)
    
    ########## methods  ##############


    
        #Finish for the day button
    def button_event():
        print("Everything saved!") #<- change this to actually save everything!! call a save all method that calls all the save methods     

#TODO - drop down menu for project tasks that shows tasks from that project in middle frame, project can only be selected if monthly focus aligns and once set cant be unset until....
#TODO - finish for the day button should be turned into a save progress, it also should have an entry below it that takes nots and feeling 1-10





 ############################################################################################       

if __name__ == "__main__":
    TaskTracking.set_display_task(washing)#<- testing purposes only 


    app = App()
    app.title("Tasker")
    #app.iconify()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()


