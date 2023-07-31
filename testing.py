""" import tkinter as tk
import pickle

class MyApp:
    def __init__(self, root):
        self.root = root
        self.string_list = []
        self.load_data()  # Load saved data from file
        
        # Create GUI elements
        self.entry = tk.Entry(root)
        self.entry.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_string)
        self.save_button.pack()

        self.clear_button = tk.Button(root, text="Clear List", command=self.clear_list)
        self.clear_button.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()

        # Display saved strings
        for item in self.string_list:
            self.listbox.insert(tk.END, item)

        # Configure window close event to save data
        self.root.protocol("WM_DELETE_WINDOW", self.save_data)

    def save_string(self):
        string = self.entry.get()
        self.string_list.append(string)
        self.listbox.insert(tk.END, string)
        self.entry.delete(0, tk.END)

    def clear_list(self):
        self.string_list.clear()
        self.listbox.delete(0, tk.END)

    def save_data(self):
        with open("data.pickle", "wb") as file:
            pickle.dump(self.string_list, file)
        self.root.destroy()

    def load_data(self):
        try:
            with open("data.pickle", "rb") as file:
                self.string_list = pickle.load(file)
        except FileNotFoundError:
            self.string_list = []

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
 """

""" import customtkinter



entry = customtkinter.CTkEntry(app, placeholder_text="CTkEntry") """
##########################################################################
# import tkinter as tk

# def button_clicked(event):
#     button_text = event.widget["text"]
#     print("Button clicked:", button_text)

# root = tk.Tk()

# text_widget = tk.Text(root)
# text_widget.pack()

# # Insert some text
# text_widget.insert("end", "This is some text.")

# # Create a button as a tag
# text_widget.tag_configure("button", background="lightblue", foreground="black")

# # Add a button within the text widget
# text_widget.insert("end", " Button ", ("button",))
# text_widget.tag_bind("button", "<Button-1>", button_clicked)

# root.mainloop()
#######################################################################################




""" is there a way to edit the following code so that when the "button text" is clicked it gets an attribute from the class instance that was used to create that text """
## this one works well
""" import tkinter as tk

class MyClass:
    def __init__(self, name):
        self.name = name

def on_text_click(event):
    line_index = text_box.index(tk.CURRENT)
    instance_index = int(line_index.split('.')[0]) - 1
    attribute = instances[instance_index].name
    print(attribute) #need to return this and use it with the display task setter

instances = [MyClass("Instance 1"), MyClass("Instance 2"), MyClass("Instance 3")]

root = tk.Tk()

text_box = tk.Text(root, height=10, width=30)
text_box.pack()

for instance in instances:
    text = instance.name
    text_box.insert(tk.END, text + "\n")

text_box.tag_configure("clickable", foreground="blue")
text_box.tag_bind("clickable", "<ButtonRelease-1>", on_text_click)

for i in range(1, len(instances) + 1):
    line_start = f"{i}.0"
    line_end = f"{i + 1}.0"
    text_box.tag_add("clickable", line_start, line_end)

root.mainloop()
 """
""" 
import tkinter as tk

root = tk.Tk()

# Create a Frame to hold the title and text box
frame = tk.Frame(root)
frame.pack()

# Create a Label for the title
title_label = tk.Label(frame, text="Title:")
title_label.pack(side=tk.LEFT)

# Create a Text widget for the text box
text_box = tk.Text(frame, width=30, height=10)
text_box.pack()

root.mainloop()
 """

""" import pickle
def save_closing_date(closing_date):

    #save files with pickle
    with open("closing_date.pkl", "wb") as file:
        pickle.dump(closing_date, file)

    # load files with pickle
    with open("closing_date.pkl", "rb") as file:
        closing_date = pickle.load(file)

    print("Saved Closing date as: ", closing_date) """



""" import pickle

duration = 0

#save files with pickle
with open("duration.pkl", "wb") as file:
    pickle.dump(duration, file)

# load files with pickle
with open("duration.pkl", "rb") as file:
    duration = pickle.load(file)

print(duration)

 """





""" #protocol method of tkinter allows callback functions for specic window manager events such as closing 

def on_close():
    #Clean up actions go here
    print("actions performed on clean up")
    root.destroy() # this is the callback function

root = tk.TK()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()  """

######################## SAVING THE CLOSING DATE ON CLOSE #################################
""" import tkinter as tk
import time
import pickle

def on_close():
    # Get the current date in the format "day-month-year"
    closing_date = time.time()
    
    # Serialize and save the closing date to a file
    with open("closing_date.pkl", "wb") as file: # stored as a float
        pickle.dump(closing_date, file)
        print(f"closing_date.pkl file saved contents: {closing_date}")
    
    # Close the Tkinter app
    root.destroy()

# Create a Tkinter root window
root = tk.Tk()

# Set the protocol for the 'WM_DELETE_WINDOW' event to the on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Create a button to close the app
close_button = tk.Button(root, text="Close App", command=on_close)
close_button.pack()

# Start the Tkinter main event loop
root.mainloop() """
################################################################
""" def update_duration():
    pass


import time

time1 = time.time()
time.sleep(4)
time2 = time.time()

# Calculate the difference between the timestamps as a float
time_difference = time2 - time1

# Extract the number of whole days from the timedelta and round it to the nearest integer
whole_days = round(time_difference / (24 * 60 * 60))  # 24 hours * 60 minutes * 60 seconds

print("Nearest number of whole days:", whole_days) """

import pickle

# habit1 = "0"
# habit2 = "0"
duration = 0
# focus1 = "Month Focus1"
# focus2 = "Month Focus2"

def load_file(file_name):
    try:
        with open(file_name, "rb") as file:
            loaded_file = pickle.load(file)
            print(f"{file_name} successfully loaded:{loaded_file}")
            return loaded_file
    
    except(FileNotFoundError, pickle.UnpicklingError):
        print("Error with 'duration' file load")

def save_file (file_name, varible):
    try:
        with open(file_name, "wb") as file:
            pickle.dump(varible, file)
        print(f"{varible} successfully saved to '{file_name}'")

    except (PermissionError, FileNotFoundError, pickle.PicklingError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__} - {e}")

#set duration file to "0"
save_file("duration.pkl", duration )
#set duration save files to "0"'s both files
# save_file("habit1.pkl", habit1)
# save_file("habit2.pkl", habit2)

# set focus1/2 files to above focus1/2 variables
# save_file("focus1.pkl", focus1)
# save_file("focus2.pkl", focus2)

""" import time
import calendar
def remaining_days_of_month():
    # Step 1: Get the current time in seconds since the epoch
    current_time = time.time()

    # Step 2: Get the current time in a structured time format (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    current_struct_time = time.localtime(current_time)
    print(current_struct_time)

    # Step 3: Calculate the last day of the month
    _, last_day = calendar.monthrange(current_struct_time.tm_year, current_struct_time.tm_mon)

    # Step 4: Calculate the remaining days
    remaining_days = last_day - current_struct_time.tm_mday

    return remaining_days

# Call the function and get the remaining days
remaining_days = remaining_days_of_month()
print("Remaining days of the month:", remaining_days) """
