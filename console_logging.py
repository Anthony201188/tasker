
import tkinter as tk
from tkinter import scrolledtext
import datetime
import io
from contextlib import redirect_stdout

def log_session(func):
    def wrapper(log_filename):
        now = datetime.datetime.now()

        with open(log_filename, "a") as log_file:
            log_file.write(f"|open,{now.strftime('%d-%m-%Y,%H:%M:%S')}|\n")

            redirected_output = io.StringIO()
            with redirect_stdout(redirected_output):
                app = func(redirected_output)
                app.start()

            log_file.write(redirected_output.getvalue())
            log_file.write(f"|close,{now.strftime('%d-%m-%Y,%H:%M:%S')}|\n")
    return wrapper

class App:
    def __init__(self, redirected_output):
        self.redirected_output = redirected_output
        self.root = tk.Tk()
        self.root.title("Console Output Logging")

        self.text_widget = scrolledtext.ScrolledText(self.root)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        self.button = tk.Button(self.root, text="Print Test", command=self.print_test)
        self.button.pack()

    def print_test(self):
        print("Test")
        self.update_text_widget()

    def update_text_widget(self):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.redirected_output.getvalue())

    def start(self):
        self.root.mainloop()

# Decorator for logging session
@log_session
def run_app(redirected_output):
    return App(redirected_output)

# Specify the log filename
log_filename = "session_log.txt"

# Run the app with logging
run_app(log_filename)




