################ methods ######################
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

    def insert_tasks(self, strings, *insert_entries):
        """ 
        Takes a single string or list of strings and the entries to populate as arguments.
        Deletes the current text and inserts the elements (str) into the insert_entries.
        Note: If multiple entries are passed to insert, type=tuple.
        """
        # Convert strings to a list of strings if it's a single string
        if isinstance(strings, str):
            strings = [strings]

        # Delete the current text #<-might not be needed
        for self.entry in insert_entries:
            self.entry.delete(0, "end")

        # Insert the strings into the insert_entries at the beginning
        for args in strings:
            for self.entry in insert_entries:
                self.entry.insert(0, args)



