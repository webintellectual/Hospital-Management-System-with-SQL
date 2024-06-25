import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
import mysql.connector
from tkinter import font
from constants import *



class Admin_add_doctors(tk.Toplevel):
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
        self.title("ADMIN-ADD DOCTORS (admin_add_doctors.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/Admin_add_doctors.png')
        # Load the image with PIL
        image = Image.open('Images/Admin_add_doctors.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        inter_font = font.Font(family="Inter")
        
#--------------------------------------- BUTTON/ Labels ------------------------------------------------------------

        self.photo = ImageTk.PhotoImage(Image.open("Images/admin_add_doctors_Add-details_button.png").resize((230, 60), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45, 30), Image.BICUBIC))


        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=lambda: self.back_button(username, password))
        self.backbutton.place(width=45,height=30,x=22.5,y=21)

        self.add_details_button = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: authenticate(self.name_entry.get(),age_entry.get(),gender_entry.get(),email_entry.get(),phone_entry.get(),specialization_entry.get(),passwrd_entry.get(),username_entry.get()))
        self.add_details_button.place(width=230,height=60,x=800,y=240)

        gap = 18

        self.name_var = tk.StringVar()
        self.name_entry = Entry(self,textvariable=self.name_var,font=(inter_font,25))
        self.name_entry.place(width=257,height=37.5,x=347,y=67)

        self.age_var = tk.StringVar()
        age_entry = Entry(self,textvariable=self.age_var,font=(inter_font,25))
        age_entry.place(width=257,height=37.5,x=347,y=67+37.5+gap)

        self.gender_var = tk.StringVar()
        gender_entry = Entry(self,textvariable=self.gender_var,font=(inter_font,25))
        gender_entry.place(width=257,height=37.5,x=347,y=67+((37.5+gap)*2))

        self.email_var = tk.StringVar()
        email_entry = Entry(self,textvariable=self.email_var,font=(inter_font,25))
        email_entry.place(width=257,height=37.5,x=347,y=67+((37.5+gap)*3))

        self.phone_var = tk.StringVar()
        phone_entry = Entry(self,textvariable=self.phone_var,font=(inter_font,25))
        phone_entry.place(width=257,height=37.5,x=347,y=67+((37.5+gap)*4))

        self.specialization_var = tk.StringVar()
        specialization_entry = Entry(self,textvariable=self.specialization_var,font=(inter_font,25))
        specialization_entry.place(width=257,height=37.5,x=850,y=67)

        self.passwrd_var = tk.StringVar()
        passwrd_entry = Entry(self,textvariable=self.passwrd_var,font=(inter_font,25))
        passwrd_entry.place(width=257,height=37.5,x=850,y=67+37.5+gap)

        self.username_var = tk.StringVar()
        username_entry = Entry(self,textvariable=self.username_var,font=(inter_font,25))
        username_entry.place(width=257,height=37.5,x=850,y=67+((37.5+gap)*2))



        self.treeview = ttk.Treeview(self,columns=("Username","Name","Age","Gender","Email","Phone No.","Specialization","Password"))

        self.treeview.heading("Username",text="Username")
        self.treeview.heading("Name",text="Name")
        self.treeview.heading("Age",text="Age")
        self.treeview.heading("Gender",text="Gender")
        self.treeview.heading("Email",text="Email")
        self.treeview.heading("Phone No.",text="Phone No.")
        self.treeview.heading("Specialization",text="Specialization")
        self.treeview.heading("Password",text="Password")

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Username",anchor="center",width=100)
        self.treeview.column("Name",anchor="center",width=100)
        self.treeview.column("Age",anchor="center",width=100)
        self.treeview.column("Gender",anchor="center",width=100)
        self.treeview.column("Email",anchor="center",width=100)
        self.treeview.column("Phone No.",anchor="center",width=100)
        self.treeview.column("Specialization",anchor="center",width=100)
        self.treeview.column("Password",anchor="center",width=100)


        # self.treeview.bind("<Double-1>", self.populate_entry_boxes)

        self.import_data()

        self.treeview.place(x=108,y=355,width=1002,height=310)



        def authenticate(name,age,gender,email,phone,specialization,password,username):
            if name != "" and age != "" and gender != "" and email != "" and phone != "" and specialization != "" and password != "" and username != "":
                age = int(age)
                mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
                mycursor = mydb.cursor()

                mycursor.execute("SELECT * FROM doc_details WHERE username = %s", (username,))

                res = mycursor.fetchone()
                if res: 
                    messagebox.showwarning("Error", "Data already exists!")


                else:
                    self.add_details(name,age,gender,email,phone,specialization,password,username)
                    messagebox.showinfo("Info", "Data edited successfully!")
                mycursor.close()
                mydb.close()


            else:
                messagebox.showerror("Error!", "All the Fields are compulsory.")


#----------------------------------------------------------------functions--------------------------------------------------------

    def authenticate(self,name,age,gender,email,phone,specialization,password,username):
        if name != "" and age != "" and gender != "" and email != "" and phone != "" and specialization != "" and password != "" and username != "":
            mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM doc_details WHERE username = %s", (username,))

            res = mycursor.fetchone()
            if res: 
                messagebox.showwarning("Error", "Data already exists!")


            else:
                self.add_details(name,age,gender,email,phone,specialization,password,username)
                messagebox.showinfo("Info", "Data edited successfully!")

                
                
            mycursor.close()
            mydb.close()


        else:
            messagebox.showerror("Error!", "All the Fields are compulsory.")



    def import_data(self):
        
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
        mycursor = mydb.cursor()

        query = "SELECT username, name, age, gender, email, phone, specialization, password FROM doc_details"
        mycursor.execute(query)

        rows = mycursor.fetchall()

        for row in rows:
            self.treeview.insert("","end",values=row)

        mycursor.close()
        mydb.close()



    def add_details(self,name,age,gender,email,phone,specialization,password,username):
        if name != "" and age != "" and gender != "" and email != "" and phone != "" and specialization != "" and password != "" and username != "":
            if len(phone) == 10 and phone.isnumeric() or phone == 'None':
                if len(age) < 4 and age.isnumeric() or age == 'None':
                    mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
                    mycursor = mydb.cursor()

                    query = "INSERT INTO doc_details (username, name, age, gender, email, phone, specialization, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    mycursor.execute(query,(username, name, age, gender, email, phone, specialization, password))
                    mycursor.execute("INSERT INTO employee(emp_name,username,password,mobile_no) VALUES(%s,%s,%s,%s)",(name,username,password,phone))
                    mydb.commit()

                    self.name_var.set('')
                    self.age_var.set('')
                    self.gender_var.set('')
                    self.email_var.set('')
                    self.phone_var.set('')
                    self.specialization_var.set('')
                    self.passwrd_var.set('')
                    self.username_var.set('')
                    self.name_entry.focus_set()

                    self.update_treeview()

                else:
                    messagebox.showerror("Error!", "Invalid Age.")
            else:
                messagebox.showerror("Error!", "Invalid Phone number.")
        else :
            messagebox.showerror("Error!", "All the Fields are compursory.")


    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        self.import_data()


    def back_button(self,username, password):
        from admin_main import Admin_Main
        self.withdraw()
        back = Admin_Main(username, password)
        back.mainloop()


if __name__ == "__main__":
    app = Admin_add_doctors("Demo123","Demo123")
    app.mainloop()