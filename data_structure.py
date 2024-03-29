

""" 
DATASTRUCTURE - using the datastructure below in a text file to record the set and done times of all the entries 
entry1|content:"content goes here"|S,18-08-2023,10:00:00|D,21-08-2023,15:30:00
entry2|content:"content goes here"|S,18-08-2023,10:00:00|D,21-08-2023,15:30:00

 """

 # NOTE - in future use the  ISO 8601 standard for date time which is "YYYY-MM-DD" this is not only the standard but can be searched lexographically (will still appear in date order when sorting by integer)
 # NOTE - could have also used sqlite locally but this was quite fun!

##### FOR SAVING THE INITIAL TEXT FILE ######
# entry1 = """
# entry1|S,18-08-2023,10:00:00|D,21-08-2023,15:30:00
# entry2|S,18-08-2023,10:00:00|D,21-08-2023,15:30:00
# """
# print(entry1)

# with open("entries.txt", "w") as file:
#     file.write(entry1)



####### LOADING PARSING SEARCHING THE TEXT FILE ###########
def load_parse_search_entries(file_name, search_term=None):
    """
    Takes a text file containing entries in the specified format,
    and returns a nested dictionary of parsed entries.
    
    Args:
        file_name (str): The name of the text file containing entries.
        search_term (str, optional): The entry name to search for. If provided,
            only entries with matching entry names will be included in the returned dictionary.
    
    Returns:
        dict: A dictionary of parsed entries.
    """
    entries = {}

    with open(file_name, "r") as txt_file:
        for line in txt_file:
            entry_line = line.strip().split("|")
            if len(entry_line) == 4:  # Check the split has been done correctly and entry_line has 4 elements
                entry_name = entry_line[0]
                content = entry_line[1][8:]  # Extract content, removing "content:" prefix
                set_info = entry_line[2]
                done_info = entry_line[3]

                # Extract set timestamp and done timestamp
                set_timestamp = set_info[2:]
                done_timestamp = done_info[2:]

                if search_term is None or entry_name == search_term:
                    if entry_name in entries:
                        entries[entry_name].append({
                            "content": content,
                            "set": set_timestamp,
                            "done": done_timestamp
                        })
                    else:
                        entries[entry_name] = [{
                            "content": content,
                            "set": set_timestamp,
                            "done": done_timestamp
                        }]
    return entries

# # Example usage
# parsed_entries = load_parse_search_entries("entries.txt", search_term="entry1")
# print(parsed_entries)



###### FULL LOADING PARSING AND SORTING THE TEXT FILE V2 #########
def full_load_parse_entries(file_name):
    """
        Load and parse entries from a text file.

        Args:
            file_name (str): The name of the text file containing entries.

        Returns:
            dict: A dictionary where each entry name maps to a list of parsed entries.

        Parses entries in the specified format from the given text file and organizes them
        into a dictionary structure. Each entry name serves as a key in the dictionary,
        mapping to a list of dictionaries containing parsed entry information.

        Each parsed entry dictionary has the following keys:
        - 'content': The content associated with the entry.
        - 'set': The timestamp when the entry was set.
        - 'done': The timestamp when the entry was marked as done.
        """
    
    entries = {}

    with open(file_name, "r") as txt_file:
        for line in txt_file:
            entry_line = line.strip().split("|")
            if len(entry_line) == 4:  # Check the split has been done correctly and entry_line has 4 elements
                entry_name = entry_line[0]
                content = entry_line[1][8:]  # Extract content, removing "content:" prefix
                set_info = entry_line[2]
                done_info = entry_line[3]

                # Extract set timestamp and done timestamp
                set_timestamp = set_info[2:]
                done_timestamp = done_info[2:]

                entry_data = {
                    "content": content,
                    "set": set_timestamp,
                    "done": done_timestamp
                }

                if entry_name in entries:
                    entries[entry_name].append(entry_data)
                else:
                    entries[entry_name] = [entry_data]
    return entries

# # test
# parsed_entries = full_load_parse_entries("entries.txt")
# print(parsed_entries)


def print_entries(entries_dict)->tuple:
    """ prints data in a readable format"""

    for entry_name, entry_info in entries_dict.items():
        set_timestamp = entry_info["set"]
        done_timestamp = entry_info["done"]
        print(f"Entry name:{entry_name} Set at:{set_timestamp} Done at:{done_timestamp}")

#print_entries(entries)

####### DATE STAMP SETUP ########
def get_current_time():
    import time
    current_time = time.time()
    local_time = time.localtime(current_time)
    formatted_time = time.strftime("%d-%m-%Y,%H:%M:%S", local_time)
    return formatted_time

# testing
formatted_time = get_current_time()
#print("Formatted Time:", formatted_time)

##### SAVE ENTRY (TO BE DELETED ONCE V2.0 IS IMPLEMENTED!)#######
def save_entries(entries_to_save, entry_contents):
    pass
    # """
    # Save entries and their corresponding content to a text file.

    # Args:
    #     entries_to_save lst(str): List of entry names to be saved.
    #     entry_contents lst(str): Corresponding list of content for each entry.

    # Adds timestamps to each entry and its content, formats them, and saves them
    # to a specified text file in the specified format.

    # Timestamps are generated using the get_current_time() function.
    # """
    # entry_lines = []

    # timestamp = get_current_time()

    # for entry, content in zip(entries_to_save, entry_contents):
    #     set_info = f"S,{timestamp}"
    #     done_info = f"D,{timestamp}"
    #     entry_line = f"{entry}|content:\"{content}\"|{set_info}|{done_info}"
    #     entry_lines.append(entry_line)

    # with open("entries.txt", "a") as file:
    #     for entry_line in entry_lines:
    #         file.write(entry_line + "\n")
    #         print(f"Entry line successfully saved: {entry_line}")

##### SAVE ENTRY V2.0 #### SEPERATE A SAVE ENTRIES FUNCTION FOR EACH OF THE FRAMES
def save_entries(entries_to_save, entry_contents, set_flags, done_flags,duration=None):
    """
    Save entries and their corresponding content to a text file.

    Args:
        entries_to_save lst(str): List of entry names to be saved.
        entry_contents lst(str): Corresponding list of content for each entry.
        set_flags lst(bool): List of flags indicating whether entries are "set."
        done_flags lst(bool): List of flags indicating whether entries are done.

    Adds timestamps to each entry and its content, formats them, and saves them
    to a specified text file in the specified format.

    Timestamps are generated using the get_current_time() function.
    """
    entry_lines = []

    timestamp = get_current_time()

    print("duration inside save_entries()",duration)

    recorded_duration = None

    if duration is not None:
        recorded_duration = duration

    print("duration inside save_entries point 2",)
    
    #zipping this many things together is a recipe for disaster seperate the functions per frame so conditions are easier to edit
    for entry, content, set_flag, done_flag in zip(entries_to_save, entry_contents, set_flags, done_flags):
        set_info_habits = f"S,{timestamp}|Remaining:{recorded_duration}" if set_flag else ""
        set_info_dailies = f"S,{timestamp},{recorded_duration}" if set_flag else ""
        done_info = f"D,{timestamp}" if done_flag else ""
        
        if duration:
            entry_line = f"{entry}|content:\"{content}\"|{set_info_habits}|{done_info}"
        else:
            entry_line = f"{entry}|content:\"{content}\"|{set_info_dailies}|{done_info}"
        
        entry_lines.append(entry_line)

    with open("entries.txt", "a") as file:
        for entry_line in entry_lines:
            file.write(entry_line + "\n")
            print(f"Entry line successfully saved: {entry_line}")

pass
## note: all daily entry recording should have the same number of lines so empty records should be recoded this is to make it easy on the eye

#daily habits recording function
#1# 'habit1|content:""||' -  condition: empty entry not set
#2# 'habit1|content:"habit1"||' - condition: entry has contents but not set
#3# 'habit1|content:"habit1"|S,18-01-2024,20:11:21|Remaining:1|' - condition:entry set with 1 day remaining duration
#4# 'habit1|content:"habit1"|S,18-01-2024,20:11:21|Remaining:1|D,01-01-2024,20:42:34'- condition entry set 1 remaining day habit completed for the day tickbox checked
            
#todays tasks recording function
#1# 'entry1|content:""||' - condition: emtpy entry not set          
#2# 'entry1|content:"Project1"||' - condition: entry has contents but not set        
#3# 'entry1|content:"Project1"|S,18-01-2024,20:06:07|'- condition: entry has contents and is set
#4# 'entry1|content:"Project1"|S,18-01-2024,20:06:07|D,18-01-2024,20:11:21' - condition: entry task done
#5# 'entry1|original content:"Project1 "|Remedial-content:"Project1 remedial task1 "|'- condition: entry has contents and remedial work not set        
#6# 'entry1|original content:"Project1"|Remedial-content:"Project1 remedial task1 "|S,01-01-2024,18:46:54|'- condition: entry has contents and remedial work set        
#7# 'entry1|original content:"Project1"|Remedial-content:"Project1 remedial task1 "|S,01-01-2024,18:46:54|D,18-01-2024,20:11:21'- condition: entry has contents and remedial done       
#8# 'entry1|original content:"Project1 "|Remedial-content:"Project1 remedial task2 "|- condition: more remedial work required not set (remedial switch still set, done recorded then new contents entered then set.(SAME AS #5#))
#9# 'entry1|original content:"Project1"|Remedial-content:"Project1 remedial task2 "|S,01-01-2024,18:46:54|- condition: more remedial work required set (SAME AS #6#)
#10# 'entry1|content:"Project1"|S,18-01-2024,20:06:07|- condition: all remedial work done back to original contents (SAME AS #3#)
#11# 'entry1|content:"Project1"|S,18-01-2024,20:06:07| - condition: finally original contents recorded as done and everything unlocked and rest back to state #1# (SAME AS ##)   

#monthly focus recording function
#0# 'S,18-01-2024,20:06:07|Remaining:10|'
#1# 'ParentProjectname|catagory|
#2# 'Focus1|content:"monthly focus1"'
#3# 'Focus2|content:"monthly focus2"'
            
#additional info recording function 
#0# 'Gratitude1|content:"Gratitude entry contetns1"'
#1# 'Gratitude2|content:"Gratitude entry contetns2"'
#2# 'Gratitude3|content:"Gratitude entry contetns3"'
#3# 'Gratitude4|content:"Gratitude entry contetns4"'
#4# 'Gratitude5|content:"Gratitude entry contetns5"'
#5# 'Fitness1|content:"Fitness entry contetns1"'
#6# 'Fitness2|content:"Fitness entry contetns2"'
#7# 'How you feel|content:"1-10"'
#8# 'Notes|content:"Long format notes here could be 250 charachters or more long
#8a#  more content more content more content etc... extends over multiple lines max char length 120 for readability"'
            

#combined single record function for button callback
            


























            
# testing
# entries_to_save = ["entry1", "entry2"]
# entry_contents = ["content for entry1", "content for entry2"]
# save_entries(entries_to_save, entry_contents)


############################# EXAMPLE OF SWAPPING OVER TO SQL #######################
#####################################################################################

########################## CREATE THE DATABASE ON START
# import sqlite3

# def create_entries_table():
#     """
#     Create the 'entries' table in the SQLite database.
#     """
#     conn = sqlite3.connect("entries.db")
#     cursor = conn.cursor()

#     # Create 'entries' table
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS entries (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             entry TEXT,
#             content TEXT,
#             set_flag BOOLEAN,
#             done_flag BOOLEAN,
#             timestamp DATETIME
#         )
#         """
#     )

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

# # Call the function to create the table
# create_entries_table()

# ############################ SAVE THE ENTRIES (replace the current save function in the datastructure.py)
# import sqlite3
# from datetime import datetime

# def save_entries_to_sqlite(entries_to_save, entry_contents, set_flags, done_flags):
#     """
#     Save entries and their corresponding content to an SQLite database.

#     Args:
#         entries_to_save (list): List of entry names to be saved.
#         entry_contents (list): Corresponding list of content for each entry.
#         set_flags (list): List of flags indicating whether entries are "set."
#         done_flags (list): List of flags indicating whether entries are done.
#     """
#     timestamp = get_current_time()

#     # Connect to SQLite database (creates a new one if it doesn't exist)
#     conn = sqlite3.connect("entries.db")
#     cursor = conn.cursor()

#     for entry, content, set_flag, done_flag in zip(entries_to_save, entry_contents, set_flags, done_flags):
#         set_info = f"S,{timestamp}" if set_flag else ""
#         done_info = f"D,{timestamp}" if done_flag else ""
#         entry_line = f"{entry}|content:\"{content}\"|{set_info}|{done_info}"

#         # Insert data into the database
#         cursor.execute(
#             """
#             INSERT INTO entries (entry, content, set_flag, done_flag, timestamp)
#             VALUES (?, ?, ?, ?, ?)
#             """,
#             (entry, content, set_flag, done_flag, timestamp),
#         )

#         print(f"Entry line successfully saved to SQLite: {entry_line}")

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

# # Example usage
# entries_to_save = ["entry1", "entry2", "entry3"]
# entry_contents = ["Content 1", "Content 2", "Content 3"]
# set_flags = [True, False, True]
# done_flags = [False, True, True]

# save_entries_to_sqlite(entries_to_save, entry_contents, set_flags, done_flags)
