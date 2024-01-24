import sqlite3

def dynamic_todays_tasks_entry_query_creation(tuples):
    """Return the SQL query string for inserting values into the 'MyFrame2' table in the Records.db

    Args:
    'tuples' is a tuple containing 6x nested tuples all with 5 elements each - tuple()
    - entry is a tuple of 5x string values to represent the entry name: (entry1, entry2, entry3, entry4, entry5)
    - contents is a tuple of 5x string values to represent corresponding entry contents: ('content1','content2','content3','content4','content5')
    - done_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done (sqlite doesn't support BOOL): '(0,1,0,0,1)'
    - set_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done (sqlite doesn't support BOOL): '(0,1,0,0,1)'
    - remedial_set_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done (sqlite doesn't support BOOL): '(0,1,0,0,1)'
    - remedial_content is a tuple of 5x strings: ('content1', 'content2', 'content3', 'content4', 'content5')

    Signature:
    tuples = (
        ('entry1', 'entry2', 'entry3', 'entry4', 'entry5'),
        ('content1', 'content2', 'content3', 'content4', 'content5'),
        (0, 1, 0, 0, 1),
        (0, 1, 0, 0, 1),
        (0, 1, 0, 0, 1),
        ('content1', 'content2', 'content3', 'content4', 'content5')
    )

    Example of packing tuples using packing:
    entry = ('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
    contents = ('content1', 'content2', 'content3', 'content4', 'content5')
    done_flags = (0, 1, 0, 0, 1)
    set_flags = (0, 1, 0, 0, 1)
    remedial_set_flags = (0, 1, 0, 0, 1)
    remedial_content_flags = ('content1', 'content2', 'content3', 'content4', 'content5')

    tuples = entry, contents, done_flags, set_flags, remedial_set_flags, remedial_content_flags

    Returns:
    string type sql query
    """
def todays_tasks_entry_query():
    """
    Return the fixed SQL query for inserting values into the 'MyFrame2' table in the 'Records.db' database.
    """
    query = """
    INSERT INTO MyFrame2 (
        entry1, entry2, entry3, entry4, entry5,
        content1, content2, content3, content4, content5,
        0, 1, 0, 0, 1,
        0, 1, 0, 0, 1,
        0, 1, 0, 0, 1,
        remedial_content1, remedial_content2, remedial_content3, remedial_content4, remedial_content5
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    return query

    
def test_insert_row(query,data, dbpath='/home/dci-student/Desktop/python/personal/tasker/records.db'):

    conn= sqlite3.connect(dbpath)

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("Data inserted successfully!")

    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

    finally:
        # Close the connection
     conn.close()


    
# Sample data for testing
entry = ('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
contents = ('content1', 'content2', 'content3', 'content4', 'content5')
done_flags = (0, 1, 0, 0, 1)
set_flags = (0, 1, 0, 0, 1)
remedial_set_flags = (0, 1, 0, 0, 1)
remedial_contents = ('content1', 'content2', 'content3', 'content4', 'content5')

tuples = entry, contents, done_flags, set_flags, remedial_set_flags, remedial_contents

# Call the function
query = dynamic_todays_tasks_entry_query_creation(tuples) 
print("query",query)
print("VALUES",tuples)


## debugging len error:
print(f"length of entry_name_typle:{len(entry)},{entry},types:{[type(_) for _ in entry]}")
print(f"length of contents_tuple :{len(contents)},{contents},types:{[type(_) for _ in contents]}")
print(f"length of done_flags_tuple :{len(done_flags)},{done_flags},types:{[type(_) for _ in done_flags]}")
print(f"length of set_flags_tuple:{len(set_flags)},{set_flags},types:{[type(_) for _ in set_flags]}")
print(f"length of remedial_set_tuple:{len(remedial_set_flags)},{remedial_set_flags},types:{[type(_) for _ in remedial_set_flags]}")
print(f"length of remedial_content_tuple :{len(remedial_contents)},{remedial_contents},types:{[type(_) for _ in remedial_contents]}")

test_insert_row(query,tuples)