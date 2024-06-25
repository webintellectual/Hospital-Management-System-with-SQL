import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from app_main import HMS
from constants import *


class Emp_Signup(tk.Toplevel):
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
        self.title("SIGN UP - EMPLOYEE (emp_signup.py)")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.image = tk.PhotoImage(file='Images/SIGN_UP_page.png')
        # Load the image with PIL
        image = Image.open('Images/SIGN_UP_page.png')
        # Resize the image to fit the canvas
        image = image.resize((window_width, window_height), Image.BICUBIC)
        # Convert the PIL image to a PhotoImage
        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')


#-------------------------------Entry Box-----------------------------------------------------------------

        name_var = tk.StringVar()
        name_entry = Entry(self,textvariable=name_var,font=("Roboto",25))
        name_entry.place(width=380,height=41,x=403,y=206)

        username_var = tk.StringVar()
        username_entry = Entry(self,textvariable=username_var,font=("Roboto",25))
        username_entry.place(width=380,height=41,x=403,y=206+41+38)

        passwrd_var = tk.StringVar()
        passwrd_entry = Entry(self,show="*",textvariable=passwrd_var,font=("Roboto",25))
        passwrd_entry.place(width=380,height=41,x=403,y=206+((41+39)*2))

        mob_var = tk.StringVar()
        mob_entry = Entry(self,textvariable=mob_var,font=("Roboto",25))
        mob_entry.place(width=380,height=41,x=403,y=206+((41+39)*3))

#----------------------------------------------------Buttons-----------------------------

        self.photo = ImageTk.PhotoImage(Image.open("Images/create_button.png").resize((255,44), Image.BICUBIC))
        self.photo1 = ImageTk.PhotoImage(Image.open("Images/back_button.png").resize((45,30), Image.BICUBIC))


        self.createbutton = Button(self,image=self.photo,borderwidth=0,highlightthickness=0,command=lambda: insertion(name_entry.get(),username_entry.get(),passwrd_entry.get(),mob_entry.get()))
        self.createbutton.place(width=255,height=44,x=465,y=546)

        self.backbutton = Button(self,image=self.photo1,borderwidth=0,highlightthickness=0,command=self.back_button)
        self.backbutton.place(width=45,height=30,x=22.5,y=21)


        def insertion(name,username,password,mobile):
            if name != "" and username != "" and password != "" and mobile != "":
                
                mydb = mysql.connector.connect(host="localhost",user="root",password="Sql123456",database="hmsdb")
                mycursor = mydb.cursor()

                mycursor.execute("SELECT * FROM employee WHERE username = %s",(username,))
                res = mycursor.fetchone()

                if res:
                    messagebox.showerror("Error!", "Username already exist, please try to login or use other Username.")

                else:
                    if len(mobile) == 10 and mobile.isnumeric():
                        try :
                            mycursor.execute("INSERT INTO employee(emp_name,username,password,mobile_no) VALUES(%s,%s,%s,%s)",(name,username,password,mobile))
                            mycursor.execute("INSERT INTO doc_details(name,username,password,phone) VALUES(%s,%s,%s,%s)",(name,username,password,mobile))
                            mydb.commit()
                            messagebox.showinfo("Info","Account Succesfully created.")
                            mycursor.close()
                            mydb.close()
                            self.create_button()
                        except Exception as e:
                            print(e)
                            mydb.rollback()
                            mydb.close()
                    else:
                        messagebox.showerror("Error!", "Invalid mobile number.")
            else:
                messagebox.showerror("Error!", "All the Fields are compursory.")

    def back_button(self):
        from emp import Employee
        self.withdraw()
        back = Employee()
        back.mainloop()

    def create_button(self):
        from emp import Employee
        self.withdraw()
        back = Employee()
        back.mainloop()

# if __name__ == "__main__":
#     app = Emp_Signup()
#     app.mainloop()
