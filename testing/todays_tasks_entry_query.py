import sqlite3

binding ="?,"
todays_tasks_query = f"""
INSERT INTO MyFrame2 (
    entry1, entry2, entry3, entry4, entry5,
    content1, content2, content3, content4, content5,
    done_flag1, done_flag2, done_flag3, done_flag4, done_flag5,
    set_flag1, set_flag2, set_flag3, set_flag4, set_flag5,
    remedial_set1, remedial_set2, remedial_set3, remedial_set4, remedial_set5,
    remedial_content1, remedial_content2, remedial_content3, remedial_content4, remedial_content5,
    recording_instance
) VALUES ({binding * 29} CURRENT_TIMESTAMP);
"""

monthly_focus_query = """
    INSERT INTO MyFrame3 (
        project, monthly_focus1, monthly_focus2, recording_instance
    ) VALUES (?, ?, ?, CURRENT_TIMESTAMP);
"""


#sample VALUES  data

project = ('project name',)
monthly_focus1 = ('monthly focus1',)
monthly_focus2 = ('monthly focus2',) 
test_data = project + monthly_focus1 + monthly_focus2

daily_habits_query = f"""
    INSERT INTO MyFrame(
    habit1,
    habit2,
    duration,
    done_flag1, done_flag2,
    set_on,
    days_remaining,
    timestamp
    ) VALUES ({binding *8} CURRENT_TIMESTAMP)
"""
# sample VALUES data

habit1= ('habit1',)
habit2 = ('habit2',)
duration = ('10',)
done_flags = ('1','0')
set_on = ('2024-01-24 12:34:56',)# (Year-Month-Day Hour:Minute:Second)
days_remaining = ('3',)
test_data = project + habit1 + habit2 + duration + set_on + days_remaining 

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
recording_instance
) VALUES ({binding * 18}CURRENT_TIMESTAMP);
"""
#sample VALUES data

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

    
def test_insert_row(query,data, dbpath='/home/dci-student/Desktop/python/personal/tasker/records.db'):
    """ test inserts the row of data passed in the data arg to the database in dbpath """

    conn= sqlite3.connect(dbpath)

    try:
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
        print(f"Data:{data} inserted successfully!")

    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

    finally:
        # Close the connection
     conn.close()


# Sample data for testing
entry = ('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
contents = ('content1', 'content2', 'content3', 'content4', 'content5')
done_flags = ('1','0','0','1','1')
set_flags = ('0', '1', '0', '0', '1')
remedial_set_flags = ('0', '1', '0', '0', '1')
remedial_contents = ('content1', 'content2', 'content3', 'content4', 'content5')

#test_data = entry + contents + done_flags + set_flags + remedial_set_flags + remedial_contents

#test the insertion 
print("test data",test_data)
test_insert_row(additional_info_query, test_data)
