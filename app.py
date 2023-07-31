import class_def
import pickle
import customtkinter as ctk
import time
import calendar
from link_click import ClickableLinkLabel

########################################  UTILS #####################################
"""  persistance used to save load and update stored data on opening of app """

#note ~ think I could make this more concise by putting all data in one file and loading that?
#note ~ or a change the functions here to load(file_name) and save(file_name)
# load duration file
def load_duration():
    try:
        with open("duration.pkl", "rb") as file:
            duration = pickle.load(file)
            print(f"duration.pkl successfully loaded:{duration}")
            return duration
    
    except(FileNotFoundError, pickle.UnpicklingError):
        print("Error with 'duration' file load")

def save_duration(duration):
    try:
        with open("duration.pkl", "wb") as file:
            pickle.dump(duration, file)
        print(f"Duration successfully saved to 'duration.pkl':{duration}")

    except (PermissionError, FileNotFoundError, pickle.PicklingError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__} - {e}")

# load closing date file
def load_closing_date():
    try:
        with open("closing_date.pkl", "rb") as file:
            closing_date = pickle.load(file)
            print(f"closing_date.pkl successfully loaded:{closing_date}")
            return closing_date
    
    except(FileNotFoundError, pickle.UnpicklingError):
        print("Error with 'closing_date.pkl' file load")

def save_closing_date(elapse): # elapse = elapsed time in epoch whole days
    try:
        with open("closing_date.pkl", "wb") as file:
            pickle.dump(elapse, file)
        print(f"Duration successfully saved to 'closing_date.pkl':{elapse}")

    except (PermissionError, FileNotFoundError, pickle.PicklingError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__} - {e}")

###################################### GENERIC LOAD AND SAVE #########################
def load_file(file_name):
    try:
        with open(file_name, "rb") as file:
            loaded_file = pickle.load(file)
            print(f"{file_name} successfully loaded:{loaded_file}")
            return loaded_file
    
    except(FileNotFoundError, pickle.UnpicklingError):
        print(f"Error with {file_name} file load")

def save_file (file_name, variable):
    try:
        with open(file_name, "wb") as file:
            pickle.dump(variable, file)
        print(f"{variable} successfully saved to '{file_name}'")

    except (PermissionError, FileNotFoundError, pickle.PicklingError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__} - {e}")


#####################################################################################

loaded_duration = load_duration() #<- should move this to the bottom of script and add if main name statment
loaded_closing_date = load_closing_date()

###################### DEFINING FRAMES AND WIDGETS ####################################
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
        self.label_number_of_days_remaining = ctk.CTkLabel(self,anchor=ctk.S, text=loaded_duration,width=60, height=60)
        self.label_number_of_days_remaining.grid(row=3, column=2, padx=10, pady=5)

        #Entries
        self.entry_habit1 = ctk.CTkEntry(self,placeholder_text="Habit1",width=180)
        self.entry_habit1.grid(row=1, column=0, padx=10, pady=10)

        self.entry_habit2 = ctk.CTkEntry(self,placeholder_text="Habit2",width=180)
        self.entry_habit2.grid(row=2, column=0, padx=10, pady=10)

        self.entry_duration = ctk.CTkEntry(self, placeholder_text="Duration",width=70)
        self.entry_duration.grid(row=3, column=3, padx=10, pady=10)

        #Buttons
        self.button = ctk.CTkButton(self, text="set habits",command=self.set_habits ,height=28, width=28 ) 
        self.button.grid(row=1, column=3, padx=20)

        self.button2 = ctk.CTkButton(self, text="set duration",command=self.set_habit_duration, height=28, width=28 ) 
        self.button2.grid(row=2, column=3, padx=20)

        #Checkboxes
        check_var = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check = ctk.CTkCheckBox(self, text="Done", variable=check_var, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check.grid(row=1, column=2)

        check_var2 = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check2 = ctk.CTkCheckBox(self, text="Done", variable=check_var2, onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
        self.check2.grid(row=2, column=2)

        #Load the habits
        self.habit1 =load_file("habit1.pkl")
        self.habit2 = load_file("habit2.pkl")

        # configure grid system
        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(2, weight=1)

        #set

        #set the entry text on start
        self.set_entry_text_on_start(self.habit1, self.habit2)

    def set_entry_text_on_start(self, text1,text2):
        #updates duration
        self.updated_loaded_duration = load_duration()
        self.text1 = text1
        self.text2 = text2
        #inserts saved text
        self.entry_habit1.insert(0,text1)
        self.entry_habit2.insert(0,text2)
        # disables input if duration not complete
        if self.updated_loaded_duration != 0:
            self.entry_habit1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_habit2.configure(state="disabled", border_width=3, border_color="black")

    def set_habits(self):
        #updates duration
        updated_loaded_duration = load_duration()
        if updated_loaded_duration == 0:
            # Sets the entry box border and disables input
            self.entry_habit1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_habit2.configure(state="disabled", border_width=3, border_color="black")

            #gets the entry text and saves it
            habit1 = self.entry_habit1.get()
            habit2 = self.entry_habit2.get()
            save_file("habit1.pkl", habit1)
            save_file("habit1.pkl", habit2)
        else:
            print("Be patient you can't change habit until duration = 0 days")


# NOTE: set duration and set habits buttons might need to be combined
# also if duration == 0 not only do the entreis need to be renabled but the save files need to be set to empty strings to avoid old habits getting re-set automatically
    def set_habit_duration(self):#<- Python has a two pass interpreter for classes so inside a class methods and vars can be called before defined.
        set_duration = int(self.entry_duration.get())
        updated_loaded_duration = load_duration() 
        if updated_loaded_duration <= 0:
            self.entry_habit1.configure(state="normal", border_width=1, border_color="grey") # configuring the entry boxes style on, 0 duration load-up
            self.entry_habit2.configure (state="normal", border_width=1, border_color="grey") # configuring the entry boxes style on, 0 duration load-up
            self.label_number_of_days_remaining.configure (text = set_duration)
            save_duration(set_duration)
            print (f"habit duration set to:{set_duration}")
        else:
            print("Be patient you can't change habit until duration = 0 days")


#Monthly focus
class MyFrame2(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height
        self.grid_rowconfigure(10, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)

        # add widgets onto the frame
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=10)
        
        #remaining days label
        self.label2 = ctk.CTkLabel(self,anchor=ctk.S, text="Remaing days untill reset",width=60, height=60)
        self.label2.grid(row=10, column=0, padx=1, pady=5)

        #number of days
        self.label3 = ctk.CTkLabel(self,anchor=ctk.S, text="6",width=60, height=60)
        self.label3.grid(row=10, column=3, padx=10, pady=5)

        #link to Trello label
        #self.label2 = ctk.CTkLabel(self, text='<a href="https://trello.com/b/ygYRZRxw/focus">Trello focus board</a>',width=60, height=60)
        #self.label2.grid(row=2, column=0, padx=10, pady=5)

        #test click link trello
        self.label_text = 'Click here Trello "focus" board'
        self.link = "https://trello.com/b/ygYRZRxw/focus"
        self.clickable_label = ClickableLinkLabel(self, text=self.label_text, link=self.link) #<- implemented own widget class based on tkinter
        self.clickable_label.grid(row=1, column=0, padx=10, pady=5)


        #Entries
        self.entry_focus1 = ctk.CTkEntry(self,placeholder_text="Month Focus1",width=180)
        self.entry_focus1.grid(row=7, column=0, padx=10, pady=20)

        self.entry_focus2= ctk.CTkEntry(self,placeholder_text="Month Focus2",width=180)
        self.entry_focus2.grid(row=9, column=0, padx=10, pady=1)

        #Button
        self.button = ctk.CTkButton(self, text="Set focus",command=self.set_month_focus, height=28, width=28 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button.grid(row=9, column=3, padx=20)
        

        # Call the function and get the remaining days
        self.remaining_days = self.remaining_days_of_month()
        print("Remaining days of the month:", self.remaining_days)

        #set the remaining_days to label
        self.label3.configure(text=self.remaining_days)

        #Load the month focus on start
        self.load_month_focus()

######## combined set month and duration function #########
    def set_habit_and_duration(self):
        MyFrame.set_habit_duration()
        self.set_dur
        pass
##############################################################

    def set_month_focus(self):
        if self.remaining_days == 0:
            #Get content of entries
            self.focus1 = self.entry_focus1.get()
            self.focus2 = self.entry_focus2.get()

            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")

            save_file("focus1.pkl", self.focus1)
            save_file("focus2.pkl", self.focus2)
    
    def load_month_focus(self):
        self.focus1 = load_file("focus1.pkl")
        self.focus2 = load_file("focus2.pkl")

        self.entry_focus1.insert(0,self.focus1)
        self.entry_focus2.insert(0,self.focus2)

        if self.remaining_days != 0:
            self.entry_focus1.configure(state="disabled", border_width=3, border_color="black")
            self.entry_focus2.configure(state="disabled", border_width=3, border_color="black")


    def remaining_days_of_month(self):
        #Get the current time in seconds since the epoch
        self.current_time = time.time()

        #Get the current time in a structured time format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        self.current_struct_time = time.localtime(self.current_time)

        #Calculate the last day of the month
        _, self.last_day = calendar.monthrange(self.current_struct_time.tm_year, self.current_struct_time.tm_mon) # month range returns tuple of day of the week (mon0-sun6) which the month starts and the secon val is the number of days in this month

        #Step 4: Calculate the remaining days
        self.remaining_days = self.last_day - self.current_struct_time.tm_mday # struct time obj can access each elem using the ".tm_xxx" tag

        return self.remaining_days


#Todays Tasks
class MyFrame3(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)

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
        self.button_suggest = ctk.CTkButton(self, text="suggest", height=28, width=28 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button_suggest.grid(row=0, column=3, padx=20)    

        self.button_set = ctk.CTkButton(self, text="set", height=28, width=50 ) # "command=button_event" needs to be added and function created and tied to it 
        self.button_set.grid(row=1, column=3, padx=5)


        #Checkboxes
        check_var = ctk.StringVar(value="off") #need to compete the get and command events for this 
        self.check = ctk.CTkCheckBox(self, text="Done", variable=check_var,border_color="green", onvalue="on", offvalue="off") #"command=checkbox_event," needs to be added to the end 
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

#Task List
class MyFrame4(ctk.CTkFrame):
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
        self.textbox.insert("0.0", "Some example text!\n" * 50)
        self.textbox.configure(state="disabled")

        #Button
        self.button_sort = ctk.CTkButton(self, text="Sort", height=28, width=45 ) 
        self.button_sort.grid(row=0, column=3, padx=20)

#Project Task List
class MyFrame4V1(ctk.CTkFrame):
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

        #Button
        self.button_sort = ctk.CTkButton(self, text="Sort", height=28, width=45 ) 
        self.button_sort.grid(row=0, column=3, padx=20)

#Urgent Task List
class MyFrame4V2(ctk.CTkFrame):
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

        #Button
        self.button_sort = ctk.CTkButton(self, text="Sort", height=28, width=45 ) 
        self.button_sort.grid(row=0, column=3, padx=20)


#Task manager
class MyFrame5(ctk.CTkFrame):
    def __init__(self, master,text, width, height):
        super().__init__(master, width, height)
        self.val = text
        self.val2 = width
        self.val3 = height

        # configure grid system
        self.grid_rowconfigure(10) 
        self.grid_columnconfigure(3)
    
        #Label for the frame
        self.label = ctk.CTkLabel(self,anchor=ctk.N, text=self.val,width=self.val2 , height=self.val3)
        self.label.grid(row=0, column=0, padx=10, pady=5)

        #Textbox
        self.textbox = ctk.CTkTextbox(self, width=300,height=310, corner_radius=3 ) # insert at line 0 character 0
        self.textbox.grid(row=0, column=0)
        self.textbox.insert("0.0", "Task Display Window")# <- need to finish this line
        self.textbox.insert("2.0",class_def.Task.display_task)# <- need to finish this line

        #Buttons
        self.button_sort = ctk.CTkButton(self, text="View selected task", height=28, width=45 ) 
        self.button_sort.grid(row=0, column=3, padx=20,pady=20)

        self.button_sort = ctk.CTkButton(self, text="Edit selected task", height=28, width=45 ) 
        self.button_sort.grid(row=1, column=3, padx=20, pady=20)

        self.button_sort = ctk.CTkButton(self, text="Add new task", height=28, width=45 ) 
        self.button_sort.grid(row=2, column=3, padx=20,pady=20)

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

############################################ DEFINING APP CLASS ############################################

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1350x850")
        self.grid_rowconfigure(3)  # configure grid system
        self.grid_columnconfigure(2)

        #Habit Tasks Frame
        self.my_frame = MyFrame(self,"Habit Tasks", 50 , 30) # frame args size order is width, height 
        self.my_frame.grid(row=0, column=0, padx=10, pady=10 )

        #Monthly Focus Frame
        self.my_frame2 = MyFrame2(self,"Monthly Focus",300, 50)
        self.my_frame2.grid(row=0, column=2, padx=10, pady=10 )

        #Today's tasks Frame
        self.my_frame3 = MyFrame3(self, "Today's Tasks", 200, 90)
        self.my_frame3.grid(row=0, column=1, padx=10, pady=10 )

        #Task list
        self.my_frame4 = MyFrame4(self,"Task List",200, 550 )
        self.my_frame4.grid(row=1, column=1, padx=2, pady=10) 

        #Project task list
        self.my_frame4 = MyFrame4V1(self,"Project Task List",200, 550 )
        self.my_frame4.grid(row=1, column=2, padx=2, pady=10) 

        #Urgent Task list
        self.my_frame4 = MyFrame4V2(self,"Urgent/Admin Task List",200, 550 )
        self.my_frame4.grid(row=1, column=3, padx=2, pady=10,)

        #Task manager
        self.my_frame5 = MyFrame5(self,"Task Manager",300, 350)
        self.my_frame5.grid(row=1, column=0, padx=10, pady=10) 

        #Finish for the day button
        def button_event():
           print("Everything saved!") #<- change this to actually save everything!! call a save all method that calls all the save methods 

        self.button_finish = ctk.CTkButton(self, text="Finish for the day \n Save All",command=button_event, height=60, width=85 ) 
        self.button_finish.grid(row=0, column=3, padx=20)

        #############################################
        """ Set the duration based on elapsed days """ 
        # needs to be turned into a function #
        
        loaded_duration = load_duration()
        if loaded_duration == 0:
            
            print(f"0 > [{loaded_duration}] no elapse update required.")
            pass
        
        else:
            # get the elapsed number of days
            self.get_elapsed_days()
            print("get_elapsed_days() successfully called")

            # Schedule the duration update function to run every day
            self.update_duration()
            print("update_duration() successfully called")
            
            #Save updated duration
            save_duration(self.duration) 

            #Save the elapse
            save_closing_date(self.elapse)
    
    def update_duration(self):
        # Update the duration based on elapsed days
        self.whole_elapsed_days = self.elapse - loaded_closing_date #<- check the maths here seems to be working backwards
        print(type(self.duration),type(self.whole_elapsed_days))
        self.duration -= self.whole_elapsed_days
        print("Number of days to deduct from duration:",self.whole_elapsed_days)

        self.my_frame.label_number_of_days_remaining.configure(text=self.duration)
        
        #re-enable entries on zero duration
        if self.duration == 0:
            self.my_frame.entry_habit1.configure(state="normal", border_width=1,)
            self.my_frame.entry_habit1.configure(state="normal", border_width=1,)
        
        else:
            # Schedule the next update after 24 hours (1 day) / after method noramlly in milliseconds(1000)
            self.after(24 * 60 * 60 * 1000, self.update_duration)
    
    def get_elapsed_days(self):

        # Set the initial duration (in days)
        self.duration = loaded_duration

        #set the loaded closing date (float)
        self.loaded_date = loaded_closing_date

        # Save the start date for duration calculation
        self.start_date = time.time()

        # Calulate the difference between closing date and date now.
        self.difference = self.start_date - self.loaded_date
        print("Float difference in seconds", self.difference)

        # Extract the number of whole days from the time float.
        self.elapse = round(self.difference / (24 * 60 * 60))  # 24hrs * 60m * 60s #<- IMPORTANT watch for errors, should change duration by 1 @ 1400 CET as the epoch time runs from UTC
        print("Elapsed epoch days:",self.elapse) #note this will be an epoch number of days ala "19562" @ time of writing
        



 ############################################################################################       

app = App()
app.title("Tasker")
#app.iconify()
app.mainloop()


