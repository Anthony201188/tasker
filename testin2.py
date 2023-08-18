""" import pickle
import os
daily_task_entry_lst = [
{"entry_name":"entry","content":"test123" ,"load_on_start":True},
{"entry_name":"entry2","content":"test345" ,"load_on_start":True},
{"entry_name":"entry3","content":"test789" ,"load_on_start":False},
]

with open("daily_task_entry_lst.pkl", "wb") as file:
    pickle.dump(daily_task_entry_lst, file)

 """


# def load_required_file(file_path):
#     """ checks whether the file needs to be loaded or not, returns the contents of the bin file as a python var """
#     with open(file_path, 'rb') as file:
#         data = pickle.load(file)
#         if data.get("load_on_start", False): #<-second param here is default val
#                 return data
#         else:
#             print(f"File [{file_path}] not required to be loaded")


# # Example usage
# contents = load_required_file("daily_task_entry.pkl")
# print(contents) 

# import os
# current_directory = os.getcwd()
# daily_task_files = [os.path.join(root, file) for root, _, files in os.walk(current_directory) for file in files if "daily_task" in file]

# print(daily_task_files)

# if daily_task_files:
#     print("Daily task files found:")
#     for file in daily_task_files:
#         print(file)
# else:
#     print("No daily task files found in the current directory and its subdirectories.")
