import inspect

def get_method_names(script):
    """ inspect a script and make a list of all method names """
    method_names = []
    # Inspect the script module to get all members (functions and classes)
    members = inspect.getmembers(script, inspect.isfunction)
    
    # Filter out the built-in functions
    for name, _ in members:
        if not name.startswith('__'):
            method_names.append(name)
    
    return method_names

# Replace 'your_script' with the name of your Python script (without the .py extension)
import app

all_method_names = get_method_names(app)
print(all_method_names)
