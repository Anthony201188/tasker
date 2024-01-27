import sqlite3
import time

# NOTE - in future use the  ISO 8601 standard for date time which is "YYYY-MM-DD" this is not only the standard but can be searched lexographically (will still appear in date order when sorting by integer)
####### DATE STAMP SETUP ########
def get_current_time():
    current_time = time.time()
    local_time = time.localtime(current_time)
    formatted_time = time.strftime("%Y-%m-%d,%H:%M:%S", local_time)
    print(f"self.habit_set_timestamp set to:{formatted_time}")
    return formatted_time

# testing
formatted_time = get_current_time()
#print("Formatted Time:", formatted_time)


class FramesMixin:
    def get_sql_query(self,frame_name):
        binding = "?,"

        """
        creates fixed sql entries for each frame 
        args: frame_name(string)
        retunrs: sql_query(string)
        """
        
        todays_tasks_query = f"""
        INSERT INTO MyFrame2 (
        entry1, entry2, entry3, entry4, entry5,
        content1, content2, content3, content4, content5,
        done_flag1, done_flag2, done_flag3, done_flag4, done_flag5,
        set_flag1, set_flag2, set_flag3, set_flag4, set_flag5,
        remedial_set1, remedial_set2, remedial_set3, remedial_set4, remedial_set5,
        remedial_content1, remedial_content2, remedial_content3, remedial_content4, remedial_content5,
        recording_instance
        ) VALUES ({binding *30 } CURRENT_TIMESTAMP);
        """
        #sample VALUES data
        """ 
        #Sample data for testing
        entry = ('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
        contents = ('content1', 'content2', 'content3', 'content4', 'content5')
        done_flags = ('1','0','0','1','1')
        set_flags = ('0', '1', '0', '0', '1')
        remedial_set_flags = ('0', '1', '0', '0', '1')
        remedial_contents = ('content1', 'content2', 'content3', 'content4', 'content5')
        """
        #sample save
        """
        test_data = entry + contents + done_flags + set_flags + remedial_set_flags + remedial_contents
        instanceofDatabaseMixin.save_entry_to_database(query,data)
        """

        monthly_focus_query = f"""
        INSERT INTO MyFrame3 (
        project,
        monthly_focus1, 
        monthly_focus2, 
        timestamp
        ) VALUES ({binding *3} CURRENT_TIMESTAMP);
        """
        #sample VALUES  data
        """ 
        project = ('project name',)
        monthly_focus1 = ('monthly focus1',)
        monthly_focus2 = ('monthly focus2',) 
        test_data = project + monthly_focus1 + monthly_focus2
        """


        daily_habits_query = f"""
        INSERT INTO MyFrame(
        habit1,
        habit2,
        set_duration,
        done_flag1, done_flag2,
        set_on,
        days_remaining,
        timestamp
        ) VALUES ({binding *7} CURRENT_TIMESTAMP)
        """
        # sample VALUES data
        """
        # sample VALUES data

        habit1= ('habit1',)
        habit2 = ('habit2',)
        set_duration = ('10',)
        done_flags = ('1','0')
        set_on = ('2024-01-24 12:34:56',)# (Year-Month-Day Hour:Minute:Second)
        days_remaining = ('3',)
        test_data = habit1 + habit2 + duration + set_on + days_remaining 
        """

        additional_info_query = f"""
        INSERT INTO MyFrame6 (
        Gratitude1,content1,
        Gratitude2,content2,
        Gratitude3,content3,
        Gratitude4,content4,
        Gratitude5,content5,
        Fitness1,content6,
        Fitness2,content7,
        Desire,content8,
        how_you_feel,
        notes,
        timestamp
        ) VALUES ({binding * 18} CURRENT_TIMESTAMP);
        """
        #sample VALUES data
        """ 
        Gratitude1 = ('Gratitude1','Gratitude1 content')
        Gratitude2 = ('Gratitude2','Gratitude2 content')
        Gratitude3 = ('Gratitude3','Gratitude3 content')
        Gratitude4 = ('Gratitude4','Gratitude4 content')
        Gratitude5 = ('Gratitude5','Gratitude5 content')
        Fitness1 = ('Fitness1','Fitness1 content')
        Fitness2 = ('Fitness2','Fitness2 content')
        desire =('Desire1', 'destire content')
        how_you_feel = ('10',)
        notes = ('up to 250 characters of notes here as a single string',)
        test_data = Gratitude1 + Gratitude2 + Gratitude3 + Gratitude4 + Gratitude5 + Fitness1 + Fitness2 + desire + how_you_feel + notes
        print(f"len test_data:{len(test_data)}") 
        """


        frame_names = ["todays_tasks", "monthly_focus", "daily_habits", "additional_info"]

        if frame_name == "todays_tasks":
            sql_query = todays_tasks_query
        elif frame_name == "monthly_focus":
            sql_query = monthly_focus_query
        elif frame_name == "daily_habits":
            sql_query = daily_habits_query
        elif frame_name == "additional_info":
            sql_query = additional_info_query
        else:
            print(f"Error: frame name[{frame_name}] not found in {frame_names}. Please check and try again")
            return None

        return sql_query

class DatabaseMixin:
    """Handles database operations."""

    def save_entry_to_database(self, data, query, dbpath='/home/dci-student/Desktop/python/personal/tasker/records.db'):
        """Attempts to save data VALUES to the database."""
        
        # Type casting for ValueErrors
        dbpath = str(dbpath)
        print("dbpath:",dbpath)
        print("data to pass:", data)
        print("query to pass:", query)

        # Creates the required SQL entry to pass to the database
        conn = sqlite3.connect(dbpath)

        try:
            cursor = conn.cursor()
            cursor.execute(data, query)  
            conn.commit()
            print("Data inserted successfully!")

        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

        finally:
            # Close the connection
            conn.close()
            print("Connection successfully closed")   



class RecordFrame(FramesMixin, DatabaseMixin):
    """Uses mixins to create the entries and pass them to the database."""

    def __init__(self, data=None):
        super().__init__()
        self.data = data

    def create_entry(self, frame_name, data):
        """Saves required data to the frame provided."""
        # Debugging
        print(f"frame_name: {frame_name}")
        print(f"data: {data}")
        
        # Set the data for this instance
        self.data = data

        sql = self.get_sql_query(frame_name)
        print(f"sql:",sql)
        self.save_entry_to_database(sql, data)


##########TESTING#################



############## CREATION OF RECORDS.DB ########################

class CreateRecordsDB:
    def __init__(self):
        #create all tables using create_table x 5
        self.create_all_tables()


    def create_table(self, table_type, frame_name, num_entries, entry_names):
        """
        Create a table based on the provided parameters.

        Parameters:
        - table_type (str): The type of table to create ("daily_habits", "monthly_focus", "todays_task", "additional_info").
        - frame_name (str): The name of the table.
        - num_entries (int): The number of entries for dynamic column generation.
        - entry_names (list): A list of entry names for dynamic column generation.

        Returns:
        None

        Sig:create_table("daily_habits", "daily_habits_table", 5, ["entry1", "entry2", "entry3", "entry4", "entry5"])
        """

        self.table_type = table_type
        self.frame_name = frame_name
        self.num_entries = num_entries
        self.entry_names = entry_names

        conn = sqlite3.connect("records.db")  # will create new if not existing
        cursor = conn.cursor()
        
        # Construct the column definitions dynamically based on the number of entries

        #Dynamic entry name and entry contents - join elements from list with ', ' as seperator
        dynamic_entry_and_contents = ', '.join([
        f'{entry_names[i]} TEXT NULL, content{i+1} TEXT NULL ' for i in range(self.num_entries) 
        ])

        
        # Dynamic remedial content
        remedial_content = ', '.join([
        f'remedial_content{i+1} TEXT NULL ' for i in range(self.num_entries )
        ])

        #Dynamic done flags
        done_flags_boolean = ', '.join([
            f'done_flag{i+1} INTEGER NULL ' for i in range(self.num_entries )
        ])

        # Dynamic set flags
        set_flags_boolean = ', '.join([
        f'set_flag{i+1} INTEGER NULL ' for i in range(self.num_entries )
        ])

        #Dynamic remdial set
        remedial_set = ', '.join([
            f'remedial_set{i+1} INTEGER NULL ' for i in range(self.num_entries )
        ])


        # Daily tasks table def
        todays_tasks_definition = f"""
        CREATE TABLE IF NOT EXISTS {self.frame_name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {dynamic_entry_and_contents},
            {done_flags_boolean},
            {set_flags_boolean},
            {remedial_set},
            {remedial_content},
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP


        );
        """


        # Monthly Focus table def
        monthly_focus_definition =f"""
            CREATE TABLE IF NOT EXISTS {self.frame_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project VARCHAR(90),
                monthly_focus1 VARCHAR(90),
                monthly_focus2 VARCHAR(90),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        );
        """

        
        #Daily habits
        daily_habits_definition =f"""
            CREATE TABLE IF NOT EXISTS {self.frame_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                habit1,
                habit2,
                set_duration INTEGER,
                {done_flags_boolean},
                set_on DATETIME,
                days_remaining INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        );
        """

        #Additional info def
        additional_info_definition =f"""
            CREATE TABLE IF NOT EXISTS {self.frame_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {dynamic_entry_and_contents},
                how_you_feel INTEGER,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        

        ######## CONDTIONALLY CREATE TABLES ########
        success = f"{self.table_type} successfully created"

        # Create daily_habits table
        if self.table_type == "daily_habits":
            cursor.execute(daily_habits_definition)
            print(success)

        #create monthly_habits table
        elif self.table_type == "monthly_focus":
            cursor.execute(monthly_focus_definition)
            print(success)
        
        elif self.table_type == "todays_tasks":
            cursor.execute(todays_tasks_definition)
            print(success)

        elif self.table_type == "additional_info":
            cursor.execute(additional_info_definition)
            print(success)
        
        else:
            print(f"Error 'data_structure.py/self.table_type/line_327':table_type not found:[{self.table_type}]")


        #close conn
        conn.commit()
        conn.close()
        print("connection closed")
      

    def create_all_tables(self):
        """ creates all x5 tables required for recording all frames and a record instance with timetable"""

        #create habit_tasks table
        self.create_table("daily_habits", "MyFrame", 2, ["habit1", "habit2"])

        #create monthly_focus table
        self.create_table("monthly_focus", "MyFrame3", 3, ["Project", "Month_Focus1", "Month_Focus2"])

        #create today_tasks table
        self.create_table("todays_tasks", "MyFrame2", 5, ["project", "urgent1", "urgent2", "non_urgent1", "non_urgent2"])

        #create addional info table
        self.create_table("additional_info", "MyFrame6", 8, ["Gratitude1", "Gratitude2", "Gratitude3", "Gratitude4", "Gratitude5","Fitness1","Fitness2","Desire"])


    ################CREATE ALL TABLES#########################
#instantiate the Recorder class creating all tables as required via contructor
#recorder = CreateRecordsDB()    
        
#######################RECORD RECORDS ########################

     


    


  