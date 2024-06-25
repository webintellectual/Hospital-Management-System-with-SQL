import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from tkinter import font
from constants import *


class patient_Profile(tk.Toplevel):
    def __init__(self,username,password, master=None):
        super().__init__(master)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        position_top = int(screen_height / 3 - window_height / 3)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.title("PATIENT-PROFILE (patient_profile.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/patient_profile.png')
        # Load the image with PIL
        image = Image.open('Images/patient_profile.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        
# ------------------------------------inserting fonts --------------------------------------------------------------------   
    
        inter_font = font.Font(family="Inter")


#----------------------------------------------------------------MySQL connection --------------------------------------------
        
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
        mycursor = mydb.cursor()

        query = "SELECT * FROM pat_details WHERE username = %s AND password = %s"
        mycursor.execute(query, (username,password))

        row = mycursor.fetchone()

        if row:
            username = row[0]
            name = row[1]
            age  = row[2]
            gender = row[3]
            email = row[4]
            phone = row[5]
            blood_grp = row[6]
            password = row[7]

        mycursor.close()
        mydb.close()


#--------------------------------------------- Creating Labels / Buttons --------------------------------------------------------

        username_label = tk.Label(self,text=username,font=(inter_font,26),bg="#9FBFC1")
        username_label.place(x=535,y=115)

        name_label = tk.Label(self,text=name,font=(inter_font,26),bg="#9FBFC1")
        name_label.place(x=535,y=115+37+17)

        age_label = tk.Label(self,text=age,font=(inter_font,26),bg="#9FBFC1")
        age_label.place(x=535,y=115+(37*2)+(17*2))

        gender_label = tk.Label(self,text=gender,font=(inter_font,26),bg="#9FBFC1")
        gender_label.place(x=535,y=115+(37*3)+(17*3))

        email_label = tk.Label(self,text=email,font=(inter_font,26),bg="#9FBFC1")
        email_label.place(x=535,y=115+(37*4)+(17*4))

        phone_label = tk.Label(self,text=phone,font=(inter_font,26),bg="#9FBFC1")
        phone_label.place(x=535,y=115+(37*5)+(17*5))

        blood_grp_label = tk.Label(self,text=blood_grp,font=(inter_font,26),bg="#9FBFC1")
        blood_grp_label.place(x=535,y=115+(37*6)+(17*6))

        password_label = tk.Label(self,text=password,font=(inter_font,26),bg="#9FBFC1")
        password_label.place(x=535,y=115+(37*7)+(17*7))



        self.photo = ImageTk.PhotoImage(Image.open("Images/adm_pro_Edit_details_button.png").resize((175, 46), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45, 30), Image.BICUBIC))

        self.edit_details_button = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: self.edit_button(username, password))
        self.edit_details_button.place(width=175,height=46,x=512,y=611)

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=lambda: self.back_button(username, password))
        self.backbutton.place(width=45,height=30,x=22.5,y=21)

        

#--------------------------------------------------------------------Functions defined -----------------------------------------------------------------------------------

    def back_button(self,username,password):
        from patient_main import pat_Main
        self.withdraw()
        back = pat_Main(username,password)
        back.mainloop()


    def edit_button(self,username,password):
        from patient_profile_update import pat_Profile_update
        self.withdraw()
        edit = pat_Profile_update(username,password)
        edit.mainloop()


# if __name__ == "__main__":
#     app = patient_Profile("Demo123","Demo123")
#     app.mainloop()
