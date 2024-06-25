import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from constants import *


class Emp_pat_hist(tk.Toplevel):
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
        self.title("DOCTOR-DASHBOARD (doctor_pat_hist.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/doctor_patient_history.png')
        # Load the image with PIL
        image = Image.open('Images/doctor_patient_history.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')


#---------------------------------------------------------------------Button-------------------------------------------------------------------------

        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45, 30), Image.BICUBIC))

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=lambda: self.back_button(username, password))
        self.backbutton.place(width=45,height=30,x=22.5,y=21)



#--------------------------------------------------------------------------Tree view-------------------------------------------------------------------

        self.treeview = ttk.Treeview(self,columns=("Patient","Date","Problem","Medicines"))

        self.treeview.heading("Patient",text="Patient")
        self.treeview.heading("Date",text="Date")
        self.treeview.heading("Problem",text="Problem")
        self.treeview.heading("Medicines",text="Medicines")
        

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Patient",anchor="center",width=120)
        self.treeview.column("Date",anchor="center",width=120)
        self.treeview.column("Problem",anchor="center",width=120)
        self.treeview.column("Medicines",anchor="center",width=120)
        

        self.import_data(username)

        self.treeview.place(x=100,y=102,width=1000,height=526)



#-----------------------------------------------------Funtions--------------------------------------------------------------------

    def import_data(self,username):
        
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
        mycursor = mydb.cursor()
        

        query = "SELECT p.username, p.pat_name, a.date, a.problem, a.medicines FROM pat_activity a INNER JOIN patient p ON a.username = p.username WHERE a.doctor = %s"
        mycursor.execute(query,(username,))

        rows = mycursor.fetchall()

        for row in rows:
            self.treeview.insert("","end",values=row[1:])

        mycursor.close()
        mydb.close()



    def back_button(self,username,password):
        from emp_main import Emp_Main
        self.withdraw()
        back = Emp_Main(username,password)
        back.mainloop()

# if __name__ == "__main__":
#     app = Emp_pat_hist("Demo123","Demo123")
#     app.mainloop()