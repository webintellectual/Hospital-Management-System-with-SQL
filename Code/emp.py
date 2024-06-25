import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
import mysql.connector
from constants import *


class Employee(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        position_top = int(screen_height / 3 - window_height / 3)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.title("EMPLOYEE LOGIN (emp.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/Login_page.png')
        # Load the image with PIL
        image = Image.open('Images/Login_page.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')


#-------------------------------Entry Box-----------------------------------------------------------------

        username_var = tk.StringVar()
        username_entry = Entry(self,textvariable=username_var,font=("Roboto",25))
        username_entry.place(width=405,height=60,x=390,y=285)

        passwrd_var = tk.StringVar()
        passwrd_entry = Entry(self,show="*",textvariable=passwrd_var,font=("Roboto",25))
        passwrd_entry.place(width=405,height=60,x=390,y=285+60+50)

#----------------------------------------------------Buttons-----------------------------

        self.photo = ImageTk.PhotoImage(Image.open("Images/adm_login_button.png").resize((170,47), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/adm_signup_button.png").resize((170,47), Image.BICUBIC))
        self.photo2 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45,30), Image.BICUBIC))


        self.loginbutton = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: authenticate(username_entry.get(),passwrd_entry.get()))
        self.loginbutton.place(width=170,height=47,x=507,y=485)

        self.signupbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=self.signup_button)
        self.signupbutton.place(width=170,height=47,x=507,y=485+47+47)

        self.backbutton = Button(self,image=self.photo2,borderwidth=0,highlightthickness=0,command=self.back_button)
        self.backbutton.place(width=45,height=30,x=22.5,y=21)



        def authenticate(username,password):

            mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM employee WHERE username = %s AND password = %s", (username, password))

            res = mycursor.fetchone()
            if res: 
                messagebox.showinfo("Login", "Login successful!")
                mycursor.close()
                mydb.close()
                self.login_button(username,password)


            else:
                messagebox.showwarning("Login", "Invalid username or password!")



    def back_button(self):
        self.destroy()
        self.master.destroy()
        back = HMS()
        back.mainloop()


    def login_button(self,username,password):
        from emp_main import Emp_Main
        self.withdraw()
        login = Emp_Main(username,password)
        login.mainloop()
        

    def signup_button(self):
        from emp_signup import Emp_Signup
        self.destroy()
        signup = Emp_Signup()
        signup.mainloop()

# if __name__ == "__main__":
#     app = Employee()
#     app.mainloop()
