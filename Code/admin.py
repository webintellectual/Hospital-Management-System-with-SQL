import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from constants import *


class Admin(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        fields_x = 390
        fields_width = 405
        fields_height = 57.5
        fields_y = 285

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        position_top = int(screen_height / 3 - window_height / 3)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.title("ADMIN LOGIN (admin.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/Admin_Login_page.png')
        # Load the image with PIL
        image = Image.open('Images/Admin_Login_page.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)


        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        



#-------------------------------Entry Box-------------------------------------------------------------------------------------------------------------------------------------

        username_var = tk.StringVar()
        username_entry = Entry(self,textvariable=username_var,font=("Roboto",25))
        username_entry.place(width=fields_width,height=fields_height,x=fields_x,y=fields_y)

        passwrd_var = tk.StringVar()
        passwrd_entry = Entry(self,show="*",textvariable=passwrd_var,font=("Roboto",25))
        passwrd_entry.place(width=fields_width,height=fields_height,x=fields_x,y=fields_y+111.4)

#----------------------------------------------------Buttons---------------------------------------------------------------------------------------------------------------

        self.photo = ImageTk.PhotoImage(Image.open("Images/adm_login_button.png"))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png"))


        self.loginbutton = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: authenticate(username_entry.get(),passwrd_entry.get()))
        self.loginbutton.place(width=140,height=47,x=528,y=533.3)

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=self.back_button)
        self.backbutton.place(width=45,height=30,x=22.5,y=21)
        
        global username
        username = username_entry.get()
        global password
        password = passwrd_entry.get()
#----------------------------------------------------SQL DATABASE CONNECTION--------------------------------------------------------------------------------------------------------
        

        def authenticate(username,password):

            mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))

            res = mycursor.fetchone()
            if res: 
                messagebox.showinfo("Login", "Login successful!")
                mycursor.close()
                mydb.close()
                self.login_button(username,password)


            else:
                messagebox.showwarning("Login", "Invalid username or password!")

#-------------------------------------------------------------defined functions-------------------------------------------------------------------------------------------------




    def back_button(self):
        self.destroy()
        self.master.destroy()
        back = HMS()
        back.mainloop()

    def login_button(self,username,password):
        from admin_main import Admin_Main
        self.withdraw()
        login = Admin_Main(username,password)
        login.mainloop()

# if __name__ == "__main__":
#     app = Admin()
#     app.mainloop()