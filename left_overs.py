"""current_directory = os.getcwd()
daily_task_files = [os.path.join(root, file) for root, _, files in os.walk(current_directory) for file in files if "daily_task_entry" in file]
print("Files found", daily_task_files)"""

"""#read files using for loop and if "load_on_start=True"
#load files for entries
self.loaded_entries = []
for entry_dict in daily_task_entry_lst:
    loaded_entry_dict = self.if_required_load_file(entry_dict) #<- returns none causes ERROR
    if loaded_entry_dict is not None:#<- stops the none types being added to the list if files not required to be loaded
        print("Files required to load:", loaded_entry_dict)
        self.loaded_entries.append(loaded_entry_dict) """


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

## swtich capture 

    #     self.remedial_content_dict = {}
    #     self.updated_entries_dict = {}
    #    #sleep incase theres any lag on switch update
    #     sleep(1)
    #     print("original-> self.entries_dict",self.entries_dict)

    #     #update the dict
    #     for entry, bool_var in self.entries_dict.items():
    #         self.updated_entries_dict[entry.get()] = bool_var.get()
    #         print("updated -> self.entries dict returned from function", self.entries_dict)
        
    #     for entry, bool_var in self.entries_dict.items():
    #         # Check if the boolean value is True and entry has non-empty content
    #         if entry and bool_var is not None and entry != "":
    #             print("entry",entry.get())
    #             print("bool_val", bool_var.get())
    #             self.remedial_content_dict[entry] = entry.get()




""" def compare_combine(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    # Elements that are in both lists
    common_elements = list(set1 & set2)

    # Elements that are unique to each list
    unique_to_list1 = list(set1 - set2)
    unique_to_list2 = list(set2 - set1)

    #combine
    combined = common_elements + unique_to_list1

    return combined """