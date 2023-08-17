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