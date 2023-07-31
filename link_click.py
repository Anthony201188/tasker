import customtkinter as ctk
import webbrowser

class ClickableLinkLabel(ctk.CTkLabel):
    def __init__(self, parent, text, link, *args, **kwargs):
        super().__init__(parent, text=text, cursor="hand2", *args, **kwargs)
        self.link = link
        #callback to open link fuction bound to button
        self.bind("<Button-1>", self.open_link) 

    def open_link(self, event):
        webbrowser.open_new(self.link)


# Usage example
if __name__ == "__main__":
    root = ctk.CTk()

    label_text = "Click here to visit Google"
    google_link = "https://www.google.com"

    clickable_label = ClickableLinkLabel(root, text=label_text, link=google_link)
    clickable_label.pack()

    root.mainloop()