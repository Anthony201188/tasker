
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

##### SAVE ENTRY V2.0 ####
def save_entries(entries_to_save, entry_contents, set_flags, done_flags):
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

    for entry, content, set_flag, done_flag in zip(entries_to_save, entry_contents, set_flags, done_flags):
        set_info = f"S,{timestamp}" if set_flag else ""
        done_info = f"D,{timestamp}" if done_flag else ""
        entry_line = f"{entry}|content:\"{content}\"|{set_info}|{done_info}"
        entry_lines.append(entry_line)

    with open("entries.txt", "a") as file:
        for entry_line in entry_lines:
            file.write(entry_line + "\n")
            print(f"Entry line successfully saved: {entry_line}")

# testing
# entries_to_save = ["entry1", "entry2"]
# entry_contents = ["content for entry1", "content for entry2"]
# save_entries(entries_to_save, entry_contents)
