import customtkinter 





app = customtkinter.CTk()
app.geometry("400x150")

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(app, values=["option 1", "option 2"],
                                     command=combobox_callback)
combobox.set("option 2")
combobox.pack()

app.mainloop()