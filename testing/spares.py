import sqlite3

def todays_tasks_entry_query(tuples):
    """Return the SQL query string for inserting values into the 'todays_tasks' table in the Records.db
    
    args:'tuples' is a tuple containing 6x nested tuples all with 5 elements each - tuple()
        - entry is a tuple of 5x string values to represent the entry name: (entry1,entry2,entry3,entry4,entry5)
        - contents is a tuple of 5x string values to represent corresponding the entry contents: ('content1','content2','content3','content4','content5') 
        - done_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done(sqlite doesnt support BOOL): '(0,1,0,0,1)'
        - set_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done(sqlite doesnt support BOOL): '(0,1,0,0,1)'
        - remedial_set_flags is a tuple of 5x 0/1 integers to represent boolean values if tasks are done(sqlite doesnt support BOOL): '(0,1,0,0,1)'
        - remedial_content is a tuple of 5x strings: ('content1', 'content2', 'content3', 'content4', 'content5')


    signiture:tuples = 
    (('entry1', 'entry2', 'entry3', 'entry4', 'entry5'),
    ('content1', 'content2', 'content3', 'content4', 'content5'),
    (0, 1, 0, 0, 1),
    (0, 1, 0, 0, 1),
    (0, 1, 0, 0, 1),
    '("contetns1","contetns2","contetns3","contetns4","contetns5")'

    example of packing tuples using packing:
    entry = ('entry1', 'entry2', 'entry3', 'entry4', 'entry5')
    contents = ('content1', 'content2', 'content3', 'content4', 'content5')
    done_flags = (0, 1, 0, 0, 1)
    set_flags = (0, 1, 0, 0, 1)
    remedial_set_flags = (0, 1, 0, 0, 1)
    remedial_content_flags = (0, 1, 0, 0, 1)

    tuples = entry, contents, done_flags, set_flags, remedial_set_flags, remedial_content_flags

    returns: string type sql query
    
    """
    try:
        # Assuming tuples is a tuple containing 6 nested tuples
        if len(tuples) != 6 or not all(isinstance(inner_tuple, tuple) for inner_tuple in tuples):
            raise ValueError("Input format is not as expected should be tuple(inner_tuple x6)")

        # Unpack tuples
        entry_name_tuple, contents_tuple, done_flags_tuple, set_flags_tuple, remedial_set_tuple, remedial_content_tuple = tuples

        # Check if the length of each nested tuple is the same
        tuple_lengths = [
            len(inner_tuple) for inner_tuple in 
            (entry_name_tuple, contents_tuple,
            done_flags_tuple, set_flags_tuple,
            remedial_set_tuple,
            remedial_content_tuple)
            ]
        
        #Check for tuple length difference and pass to error
        if len(set(tuple_lengths)) != 1:
            
            different_lengths = [len(inner_tuple) for inner_tuple, length in zip(
                (entry_name_tuple,
                contents_tuple,
                done_flags_tuple,
                set_flags_tuple,
                remedial_set_tuple,
                remedial_content_tuple),
                tuple_lengths) 
                if length != tuple_lengths[0]]
            
            raise ValueError(f"All nested tuples must have the same length. Found different lengths in tuple: {different_lengths}")

        # Construct the main query
        query = f"""
        INSERT INTO MyFrame2 (
            {', '.join([f'{entry_name}' for entry_name in entry_name_tuple])},
            {', '.join([f'{content}' for content in contents_tuple])},
            {', '.join([f'{done_flag}' for done_flag  in done_flags_tuple])},
            {', '.join([f'{set_flag}' for set_flag in set_flags_tuple])},
            {', '.join([f'{remedial_flag}' for remedial_flag in remedial_set_tuple])},
            {', '.join([f'{remedial_content}' for remedial_content in remedial_content_tuple])}
        ) VALUES ({', '.join(['?' for _ in range(len(entry_name_tuple) * 5)])})
        """
        return query
    
    #if error occurs then return None
    except Exception as e:
        print(f"Error: {e}")
        return None 
    
def test_insert_row(query, dbpath='/home/dci-student/Desktop/python/personal/tasker/records.db'):

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
query_result = todays_tasks_entry_query(tuples) 
print(query_result) 

## debugging len error:
print(f"length of entry_name_typle:{len(entry)},{entry},types:{[type(_) for _ in entry]}")
print(f"length of contents_tuple :{len(contents)},{contents},types:{[type(_) for _ in contents]}")
print(f"length of done_flags_tuple :{len(done_flags)},{done_flags},types:{[type(_) for _ in done_flags]}")
print(f"length of set_flags_tuple:{len(set_flags)},{set_flags},types:{[type(_) for _ in set_flags]}")
print(f"length of remedial_set_tuple:{len(remedial_set_flags)},{remedial_set_flags},types:{[type(_) for _ in remedial_set_flags]}")
print(f"length of remedial_content_tuple :{len(remedial_contents)},{remedial_contents},types:{[type(_) for _ in remedial_contents]}")

test_insert_row(query_result)