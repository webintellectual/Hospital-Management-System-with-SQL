import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from tkinter import font
from patient import Patient
from constants import *


class patient_activity(tk.Toplevel):
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
        self.title("PATIENT-ACTIVITY (patient_activity.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/patient_main_activity.png')
        # Load the image with PIL
        image = Image.open('Images/patient_main_activity.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

        inter_font = font.Font(family="Inter")
#-------------------------------------------------------label / buttons----------------------------------------------------------------------------------------


        self.date_var = tk.StringVar()
        self.date_entry = Entry(self,textvariable=self.date_var,font=(inter_font,25))
        self.date_entry.place(width=270,height=37,x=305,y=101)

        self.problem_var = tk.StringVar()
        problem_entry = Entry(self,textvariable=self.problem_var,font=(inter_font,25))
        problem_entry.place(width=270,height=37,x=305,y=101+37+30)

        self.medicines_var = tk.StringVar()
        medicines_entry = Entry(self,textvariable=self.medicines_var,font=(inter_font,25))
        medicines_entry.place(width=270,height=37,x=830,y=101)

        # self.doctor_var = tk.StringVar()
        # doctor_entry = Entry(self,textvariable=self.doctor_var,font=(inter_font,25))
        # doctor_entry.place(width=350,height=50,x=1079,y=233)

        self.doctor_var = tk.StringVar()
        self.doctor_combobox = ttk.Combobox(self, textvariable=self.doctor_var, font=(inter_font, 25))
        self.doctor_combobox.place(width=270, height=37, x=830, y=101+37+30)
        
        # Populate the doctor_combobox with doctor names
        self.populate_doctor_combobox()

        



        self.photo = ImageTk.PhotoImage(Image.open("Images/patient_activity_submit_button.png").resize((200,50), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45,30), Image.BICUBIC))

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=lambda: self.back_button(username, password))
        self.backbutton.place(width=45,height=30,x=22.5,y=21)

        self.submit_button = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: self.submit(self.date_var.get(),self.problem_var.get(),self.medicines_var.get(),self.doctor_var.get(),username))
        self.submit_button.place(width=200,height=50,x=495,y=246)




#-----------------------------------------------------------Tree view-------------------------------------------------------------------------------------------

        self.treeview = ttk.Treeview(self,columns=("Date","Problem","Medicines","Doctor"))

        self.treeview.heading("Date",text="Date")
        self.treeview.heading("Problem",text="Problem")
        self.treeview.heading("Medicines",text="Medicines")
        self.treeview.heading("Doctor",text="Doctor")
        

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Date",anchor="center",width=170)
        self.treeview.column("Problem",anchor="center",width=170)
        self.treeview.column("Medicines",anchor="center",width=170)
        self.treeview.column("Doctor",anchor="center",width=170)
        

        self.import_data()

        self.treeview.place(x=86,y=342,width=1020,height=280)


    def populate_doctor_combobox(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password="Sql123456", database="hmsdb")
        mycursor = mydb.cursor()
        
        query = "SELECT username FROM doc_details"
        mycursor.execute(query)
        
        doctors = mycursor.fetchall()
        
        # Extract doctor names from the result and populate the combobox
        doctor_names = [doctor[0] for doctor in doctors]
        self.doctor_combobox['values'] = doctor_names
        
        mycursor.close()
        mydb.close()


    def import_data(self):
        
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
        mycursor = mydb.cursor()

        query = "SELECT date, problem, medicines, doctor FROM pat_activity"
        mycursor.execute(query)

        rows = mycursor.fetchall()

        for row in rows:
            self.treeview.insert("","end",values=row)

        mycursor.close()
        mydb.close()



    def submit(self,date, problem, medicines, doctor,username):
        if date != "" and problem != "" and medicines != "" and doctor != "":
            mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
            mycursor = mydb.cursor()

            query = "INSERT INTO pat_activity (username, date, problem, medicines, doctor) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(query,(username, date, problem, medicines, doctor))
            mydb.commit()

            self.date_var.set('')
            self.problem_var.set('')
            self.medicines_var.set('')
            self.doctor_var.set('')
            self.date_entry.focus_set()

            self.update_treeview()


        else :
            messagebox.showerror("Error!", "All the Fields are compursory.")



    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        self.import_data()



    def back_button(self,username,password):
        from patient_main import pat_Main
        self.withdraw()
        back = pat_Main(username,password)
        back.mainloop()

# if __name__ == "__main__":
#     app = patient_activity("Demo123","Demo123")
#     app.mainloop()

