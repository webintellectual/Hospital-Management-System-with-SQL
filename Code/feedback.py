import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import font
import mysql.connector
from app_main import HMS
from constants import *


class feedback(tk.Toplevel):
    def __init__(self,master=None):
        super().__init__(master)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        position_top = int(screen_height / 3 - window_height / 3)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.title("FITNESS CENTER (feedback.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/Feedback_page.png')
        # Load the image with PIL
        image = Image.open('Images/Feedback_page.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        self.protocol("WM_DELETE_WINDOW", self.Exit)
        
        
        inter_font = font.Font(family="Inter")

#----------------------------------------Buttons------------------------------------------------------------------------------------

        self.photo = ImageTk.PhotoImage(Image.open("Images/submit_button.png").resize((210, 56), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45, 30), Image.BICUBIC))

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=self.back_button)
        self.backbutton.place(width=45,height=30,x=22.5,y=21)


        self.name_var = tk.StringVar()
        self.name_entry = Entry(self,textvariable=self.name_var,font=(inter_font,25))
        self.name_entry.place(width=465,height=50,x=512,y=189)

        self.email_var = tk.StringVar()
        email_entry = Entry(self,textvariable=self.email_var,font=(inter_font,25))
        email_entry.place(width=465,height=50,x=512,y=189+50+20)

        self.feedback_var = tk.StringVar()
        feedback_entry = Entry(self,textvariable=self.feedback_var,font=(inter_font,25))
        feedback_entry.place(width=465,height=220,x=512,y=189+50+20+50+20)



        self.submit_button = Button(self,borderwidth=0,highlightthickness=0,image=self.photo,command=self.submit_feedback)
        self.submit_button.place(width=210, height=56, x=495, y=577)




    def submit_feedback(self):
        name = self.name_var.get()
        email = self.email_var.get()
        feedback = self.feedback_var.get()

        if name and email and feedback:
            # Insert the values into the feedback table
            mydb = mysql.connector.connect(host="localhost", user="root", password="Sql123456", database="hmsdb")
            mycursor = mydb.cursor()

            query = "INSERT INTO feedback (name, email, feedback) VALUES (%s, %s, %s)"
            values = (name, email, feedback)
            mycursor.execute(query, values)

            mydb.commit()
            mycursor.close()
            mydb.close()

            # Clear the entry boxes
            self.name_var.set("")
            self.email_var.set("")
            self.feedback_var.set("")

            messagebox.showinfo("Success", "Feedback submitted successfully!")
        else:
            messagebox.showerror("Error", "Please enter all the values.")




    def Exit(self):
        if messagebox.askyesno("Exit","Are You sure you want to exit?"):
            self.destroy()


    def back_button(self):
        self.master.destroy()
        home = HMS()
        home.mainloop()

# if __name__ == "__main__":
#     app = feedback()
#     app.mainloop()
