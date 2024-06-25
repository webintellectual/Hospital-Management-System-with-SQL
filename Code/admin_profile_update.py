import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from tkinter import font
from constants import *



class Admin_Profile_update(tk.Toplevel):
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
        self.title("ADMIN-PROFILE (UPDATE) (admin_profile_update.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/Admin_Profile_Edit.png')
        # Load the image with PIL
        image = Image.open('Images/Admin_Profile_Edit.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')


        inter_font = font.Font(family="Inter")
#-------------------------------------------------------------- Entry box / button ---------------------------------------------------------------

        gap = 14
        # ht = 37.5

        self.username_var = tk.StringVar()
        username_entry = Entry(self,textvariable=self.username_var,font=(inter_font,25),state="readonly")
        username_entry.place(width=409,height=37.5,x=520,y=150)

        self.name_var = tk.StringVar()
        name_entry = Entry(self,textvariable=self.name_var,font=(inter_font,25))
        name_entry.place(width=409,height=37.5,x=520,y=150+37.5+gap)

        self.age_var = tk.StringVar()
        age_entry = Entry(self,textvariable=self.age_var,font=(inter_font,25))
        age_entry.place(width=409,height=37.5,x=520,y=150+((37.5+gap)*2))

        self.gender_var = tk.StringVar()
        gender_entry = Entry(self,textvariable=self.gender_var,font=(inter_font,25))
        gender_entry.place(width=409,height=37.5,x=520,y=150+((37.5+gap)*3))

        self.email_var = tk.StringVar()
        email_entry = Entry(self,textvariable=self.email_var,font=(inter_font,25))
        email_entry.place(width=409,height=37.5,x=520,y=150+((37.5+gap)*4))

        self.phone_var = tk.StringVar()
        phone_entry = Entry(self,textvariable=self.phone_var,font=(inter_font,25))
        phone_entry.place(width=409,height=37.5,x=520,y=150+((37.5+gap)*5))

        self.passwrd_var = tk.StringVar()
        passwrd_entry = Entry(self,textvariable=self.passwrd_var,font=(inter_font,25))
        passwrd_entry.place(width=409,height=37.5,x=520,y=150+((37.5+gap)*6))


        self.photo = ImageTk.PhotoImage(Image.open("Images/adm_pro_Save_details_button.png").resize((200,52), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png"))

        self.save_detail_button = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=self.save_details)
        self.save_detail_button.place(width=200,height=52,x=495,y=610)

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=lambda: self.back_button(username, password))
        self.backbutton.place(width=45,height=30,x=22.5,y=21)

#------------------------------------------------------mysql connection----------------------------------------------------------

        mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
        mycursor = mydb.cursor()

        query = "SELECT * FROM admin_details WHERE username = %s"
        mycursor.execute(query, (username,))

        row = mycursor.fetchone()

        if row:
            username = row[0]
            name = row[1]
            age  = row[2]
            gender = row[3]
            email = row[4]
            phone = row[5]
            password = row[6]

        self.username_var.set(username)
        self.name_var.set(name)
        self.age_var.set(age)
        self.gender_var.set(gender)
        self.email_var.set(email)
        self.phone_var.set(phone)
        self.passwrd_var.set(password)

#-----------------------------------------------------------function define -----------------------------------------------------------------

    def save_details(self):
        username = self.username_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        password = self.passwrd_var.get()
            
        if name == "":
            name = None
        if age == "":
            age = None
        if gender == "":
            gender = None
        if email == "":
            email = None
        if phone == "":
            phone = None
        if password == "":
            password = None

        mydb = mysql.connector.connect(host="localhost", user="root", password="Sql123456", database="hmsdb")
        mycursor = mydb.cursor()

        a = b = 1  
        try:
            query = "UPDATE admin_details SET Name = %s, gender = %s, email = %s, password = %s WHERE username = %s"
            mycursor.execute(query, (name, gender, email, password, username))

            query = "UPDATE admin SET password = %s WHERE username = %s"
            mycursor.execute(query,(password,username))


            mydb.commit()

        except mysql.connector.Error as err:
            print(f"Error inserting mobile number: {err}")
        
        if age.isnumeric() and len(age) < 4:
            try:
                query = "UPDATE admin_details SET age = %s WHERE username = %s"
                mycursor.execute(query, (age,username))

                mydb.commit()

            except mysql.connector.Error as err:
                print(f"Error inserting mobile number: {err}")

        else:
            if age != 'None':
                a = 0
                messagebox.showerror("Error!", "Age is Invalid.")

        if (len(phone) == 10 and phone.isnumeric()):
            try:
                query = "UPDATE admin_details SET phone = %s WHERE username = %s"
                mycursor.execute(query, (phone,username))

                mydb.commit()

            except mysql.connector.Error as err:
                print(f"Error inserting mobile number: {err}")

        else:
            if phone != 'None':
                b = 0
                messagebox.showerror("Error!", "Phone number is Invalid.")

        if (a == 1 and b == 1):
            messagebox.showinfo("Update", "Profile details updated successfully!")
            
        mydb.commit()

        mycursor.close()
        mydb.close()


        from admin_profile import Admin_Profile
        self.withdraw()
        save = Admin_Profile(username,password)
        save.mainloop()

    
    def back_button(self,username,password):
        from admin_profile import Admin_Profile
        self.withdraw()
        back = Admin_Profile(username,password)
        back.mainloop()

# if __name__ == "__main__":
#     app = Admin_Profile_update("Demo123","Demo123")
#     app.mainloop()