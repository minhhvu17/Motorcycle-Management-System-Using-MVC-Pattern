import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import pymysql, os, re, time
from core.Core import Core
from hashlib import sha256
from views.UserSignIn import UserSignIn as UserSignIn
from views.HomeView import HomeView as HomeView
from views.UserSignIn import UserRestorePassword as UserRestorePassword

class LoginPage(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title("Login")
        # find screen width and height
        global screen_width, screen_height
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{int(self.screen_width*3/4)}x{int(self.screen_height*3/4)}")
        self.window.configure(background="#cc0000")
        self.create_background()
        self.create_widgets()
        self.move_in()
        self.window.bind("<Control-w>", lambda e: self.window.destroy())

    def create_background(self):
        frameCnt = 12
        file_name = '../img/login_page.gif'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        frames = [tk.PhotoImage(file=file_path, format=f"gif -index {i}") for i in range(frameCnt)]
        for i in range(frameCnt):
            frames[i] = frames[i].subsample(2, 2)
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            try:
                self.label.configure(image=frame)
            except:
                return
            self.window.after(50, update, ind)
        self.label = tk.Label(self.window, bg = "#cc0000")
        self.label.place(x = 10, y = 0)
        self.window.after(0, update, 0)

    def show_password(self, event, entry):
        if entry["show"] == "*":
            # show the password
            entry["show"] = ""
        else:
            entry["show"] = "*"
    
    def create_widgets(self):
        self.label_username = ttk.Label(self.window, text="Username:", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_username = tk.Entry(self.window, width=32, font=("Inconsolata", 10), background="black", bd = 2, fg="black", bg= "white")

        self.label_password = ttk.Label(self.window, text="Password: ", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_password = tk.Entry(self.window, show="*", width=32, font=("Inconsolata", 10), background="white", bd = 2, foreground="black")

        self.button_login = tk.Button(self.window, text="Login", command=self.login)
        self.button_forgot_password = tk.Button(self.window, text= "Forgot password?", activeforeground="blue")
        self.button_signup = tk.Button(self.window, text="Don't have an account? Sign Up", width=32, bg = "#ffffff", bd = 0, font=("Inconsolata", 10), underline= 1, activeforeground="red")

        self.label_username.place(relx=0.483, rely=0.5, anchor="e")
        self.entry_username.place(relx=0.41, rely=0.55, anchor="w")
        self.label_password.place(relx=0.49, rely=0.6, anchor="e")
        self.entry_password.place(relx=0.41, rely=0.65, anchor="w")
        self.button_login.place(relx=0.428, rely=0.72, anchor="center")
        self.button_forgot_password.place(relx=0.568, rely=0.72, anchor="center")
        self.button_signup.place(relx=0.511, rely=0.8, anchor="center")       
        self.button_signup.bind("<Button-1>", lambda event: self.move_out(event, self.window, 5))
        self.button_forgot_password.bind("<Button-1>", lambda event: self.move_out_fg(event, self.window, 5))
        self.window.bind("<Return>", lambda event: self.login())

        # default state is hidden
        image = '../img/close_eye.png'
        #create an image object
        file_path = os.path.join(os.path.dirname(__file__), image)
        self.hide_password_icon = tk.PhotoImage(file=file_path)
        #resize the image
        self.hide_password_icon = self.hide_password_icon.subsample(10, 10)
        #create a label to display the image
        self.hide_password = tk.Button(self.window, image=self.hide_password_icon, background="#ffffff", bd = 2)
        self.hide_password.place(relx=0.6, rely=0.651, anchor="center")        
        self.hide_password.bind("<Button-1>", lambda event: self.show_password(event, self.entry_password))

    def move_in(self):
        x = 0
        while x <= 400:
            self.label.place(x=x, y=0)
            x += 0.5
            self.window.update()
        self.label.place(x=400, y=0)
        self.label.after_cancel(self.update)

    def move_out(self, event, window, duration):
        try:
            if self.label.winfo_x() is None:
                return
            x = self.label.winfo_x()
            self.label.place(x=x+30)
            self.window.after(30, self.move_out, event, window, duration)
            if x > 1200:
                self.window.after(0, self.signup())
        except:
            return
        
    def move_out_fg(self, event, window, duration):
        try:
            if self.label.winfo_x() is None:
                return
            x = self.label.winfo_x()
            self.label.place(x=x+30)
            self.window.after(30, self.move_out_fg, event, window, duration)
            if x > 1200:
                self.window.after(0, self.forgot_password())
        except:
            return

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        #hash the password to check
        h_check = sha256()
        h_check.update(password.encode())
        password = h_check.hexdigest()

        #import time to store the time of login
        time_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if username == "" or password == "":
            messagebox.showerror("Error", "Username or password is empty")
        try:
            db = UserSignIn()
            if db.authenticate(username, password):
                messagebox.showinfo("Success", "Login successfully")
                # create a new table to store the time of login
                conn = mysql.connector.connect(
                    host="localhost",
                    user = 'root',
                    password = 'minhhvu11',
                    database = 'motorbikemanagement'
                )
                cur = conn.cursor()
                try:
                    cur.execute("CREATE TABLE login_history(username VARCHAR(255), time_login VARCHAR(255))")
                except:
                    pass
                #insert the username and time of login into the table
                cur.execute("INSERT INTO login_history(username, time_login) VALUES(%s, %s)", (username, time_login))
                conn.commit()
                conn.close()
                # switch to interface.py
                for widget in self.window.winfo_children():
                    widget.destroy()
                # self.destroy()
                try:
                    app = Core.openController("home", self.window)           
                    app.main()
                except Exception as e:
                    print(e)
            else:
                messagebox.showerror("Error", "Username or password is incorrect")
        except:
            return

    def signup(self):
        self.destroy()
        self.label.destroy()
        self.button_signup.destroy()
        self.button_forgot_password.destroy()
        self.button_login.destroy()
        self.entry_username.destroy()
        self.entry_password.destroy()
        self.label_username.destroy()
        self.label_password.destroy()
        self.hide_password.destroy()
        self.window.switch_frame(SignupPage)
    
    def forgot_password(self):
        self.destroy()
        self.label.destroy()
        self.button_signup.destroy()
        self.button_forgot_password.destroy()
        self.button_login.destroy()
        self.entry_username.destroy()
        self.entry_password.destroy()
        self.label_username.destroy()
        self.label_password.destroy()
        self.hide_password.destroy()
        self.window.switch_frame(ForgotPass)

class SignupPage(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title("Sign Up")
        global screen_width1, screen_height1
        self.screen_width1 = self.window.winfo_screenwidth()
        self.screen_height1 = self.window.winfo_screenheight()
        self.window.geometry(f"{int(self.screen_width1*3/4)}x{int(self.screen_height1*3/4)}")
        self.window.resizable(False, False)
        self.window.configure(background="#cc0000")
        self.create_background()
        self.create_widgets()
        self.move_in()

    def create_background(self):
        frameCnt = 12
        file_name = '../img/login_page.gif'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        frames = [tk.PhotoImage(file=file_path, format=f"gif -index {i}") for i in range(frameCnt)]
        for i in range(frameCnt):
            frames[i] = frames[i].subsample(1, 1)

        self.label1 = tk.Label(self.window, bg="#cc0000")
        self.label1.place(relx=0, rely=0.5, anchor="center")

        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            try:
                self.label1.configure(image=frame)
            except:
                pass
            self.window.after(100, update, ind)

        self.update = update
        self.window.after(0, self.update, 0)

    def move_in(self):
        x = 0
        while x <= 400:
            self.label1.place(x=x, y=0)
            x += 40
            self.window.update()
            time.sleep(0.08)
        self.label1.place(x=400, y=0)
        self.label1.after_cancel(self.update)

    def move_out(self, event, window, duration):
        x = 400
        try:
            while x >= 0:
                self.label1.place(x=x, y=0)
                x += 10
                self.window.update()
                self.label1.after_cancel(self.update)
                if x > 2000:
                    self.window.after(10, self.login())
        except:
            pass

    def on_entry_focus_in(self, event, entry):
        if entry.get() == "This field is required":
            entry.delete(0, "end")
            entry.insert(0, "")
        if entry.get() == "This is not a valid email":
            entry.delete(0, "end")
            entry.insert(0, "")
        if entry.get() == "DD/MM/YYYY":
            entry.delete(0, "end")
            entry.insert(0, "")
        entry.config(background="#ffffff")
    
    def on_entry_focus_out(self, event, entry):
        if entry.get() == "":
            entry.insert(0, "This field is required")
            entry.config(background="red")
        
    def validate_user(self, event, entry, regex):
        if re.match(regex, entry.get()):
            entry.config(background="#ffffff")
            entry.insert(0, "")
        else:
            entry.config(background="red")
        
    # check valid email
    def validate_email(self, event, entry):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, entry.get())):
            entry.config(background="#ffffff")
        else:
            entry.config(background="red")
            entry.delete(0, "end")
            entry.insert(0, "This is not a valid email")
    
    def validate_password(self, event, entry):
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
        if (re.fullmatch(regex, entry.get())):
            entry.config(background="#ffffff")
        else:
            entry.config(background="red")
            entry.delete(0, "end")
            entry.insert(0, "Must contain at least 8 characters, 1 uppercase, 1 lowercase and 1 number")
    
    def show_password(self, event, entry):
        if entry["show"] == "*":
            # show the password
            entry["show"] = ""
        else:
            entry["show"] = "*"

    def create_widgets(self):
        self.label_name = tk.Label(self.window, text="Full Name", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_name = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2, fg = "black", bg = "white")
        self.entry_name.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_name))
        self.entry_name.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, self.entry_name))
        self.entry_name.bind("<Key>", lambda event: self.validate_user(event, self.entry_name, "^[\w\s]+$"))

        self.label_dob = tk.Label(self.window, text="Date of Birth", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_dob = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_dob.insert(0, "DD/MM/YYYY")
        self.entry_dob.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_dob))
        self.entry_dob.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, self.entry_dob))
        self.entry_dob.bind("<Key>", lambda event: self.validate_user(event, self.entry_dob, '^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'))

        self.label_email = tk.Label(self.window, text="Email", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_email = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_email.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_email))
        self.entry_email.bind("<FocusOut>", lambda event: self.validate_email(event, self.entry_email))

        self.label_phone = tk.Label(self.window, text="Phone Number", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_phone = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_phone.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_phone))
        self.entry_phone.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, self.entry_phone))

        self.label_address = tk.Label(self.window, text="Address", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_address = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_address.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_address))
        self.entry_address.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, self.entry_address))

        self.label_username = tk.Label(self.window, text="Username", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_username = tk.Entry(self.window, width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_username.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_username))
        self.entry_username.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, self.entry_username))

        self.label_password = tk.Label(self.window, text="Password", font=("Inconsolata", 14), background="#cc0000", foreground="white")
        self.entry_password = tk.Entry(self.window, show="*", width=28, font=("Inconsolata", 10), bd = 2)
        self.entry_password.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_password))
        self.entry_password.bind("<FocusOut>", lambda event: self.validate_password(event, self.entry_password))
        
        #create an eye icon to show the password default state is hidden
        image = '../img/close_eye.png'
        #create an image object
        file_path = os.path.join(os.path.dirname(__file__), image)
        self.hide_password_icon = tk.PhotoImage(file=file_path)
        #resize the image
        self.hide_password_icon = self.hide_password_icon.subsample(9, 9)
        #create a label to display the image
        self.hide_password = tk.Button(self.window, image=self.hide_password_icon, background="#ffffff", bd = 0)
        self.hide_password.place(relx=0.835, rely=0.771, anchor="center")        
        self.hide_password.bind("<Button-1>", lambda event: self.show_password(event, self.entry_password))

        self.button_signup = tk.Button(self.window, text="Sign Up", command=self.signup)
        self.button_back = tk.Button(self.window, text="Back")
        self.button_back.bind("<Button-1>", lambda event: self.move_out(event, self.window, 5))

        #pack widgets and set the position on the background
        self.label_name.place(relx=0.7435, rely=0.1, anchor="ne")
        self.entry_name.place(relx=0.758, rely=0.181, anchor="center")

        self.label_dob.place(relx=0.773, rely=0.2, anchor="ne")
        self.entry_dob.place(relx=0.758, rely=0.271, anchor="center")

        self.label_email.place(relx=0.71, rely=0.3, anchor="ne")
        self.entry_email.place(relx=0.758, rely=0.371, anchor="center")

        self.label_phone.place(relx=0.765, rely=0.4, anchor="ne")
        self.entry_phone.place(relx=0.758, rely=0.471, anchor="center")

        self.label_address.place(relx=0.727, rely=0.5, anchor="ne")
        self.entry_address.place(relx=0.758, rely=0.571, anchor="center")

        self.label_username.place(relx=0.738, rely=0.6, anchor="ne")
        self.entry_username.place(relx=0.758, rely=0.671, anchor="center")

        self.label_password.place(relx=0.738, rely=0.7, anchor="ne")
        self.entry_password.place(relx=0.758, rely=0.771, anchor="center")

        self.button_signup.place(relx=0.715, rely=0.83, anchor="ne")
        self.button_back.place(relx=0.815, rely=0.83, anchor="nw")

    def login(self):
        self.label_name.destroy()
        self.entry_name.destroy()
        self.label_dob.destroy()
        self.entry_dob.destroy()
        self.label_email.destroy()
        self.entry_email.destroy()
        self.label_phone.destroy()
        self.entry_phone.destroy()
        self.label_address.destroy()
        self.entry_address.destroy()
        self.label_username.destroy()
        self.entry_username.destroy()
        self.label_password.destroy()
        self.entry_password.destroy()
        self.button_signup.destroy()
        self.button_back.destroy()
        self.hide_password.destroy()
        self.label1.destroy()
        self.destroy()
        self.window.switch_frame(LoginPage)

    def signup(self):
        username = self.entry_username.get()
        user_password = self.entry_password.get()
        # hash the password
        h = sha256()
        h.update(user_password.encode())
        hash = h.hexdigest()
        user_password = hash

        fullname = self.entry_name.get()
        dob = self.entry_dob.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        if username == "" or user_password == "" or fullname == "" or dob == "" or email == "" or phone == "" or address == "":
            messagebox.showerror("Error", "something is missing")
        else:
            try:
                con = pymysql.connect(host = "localhost",user="root",password="minhhvu11")
                mycursor = con.cursor()
            except:
                messagebox.showerror("Error", "Error in connection")
                return
        try:
            query = 'create database motorbikemanagement'
            mycursor.execute(query)
            query = 'use motorbikemanagement'
            mycursor.execute(query)
            try:
                query = 'create table user_data(username varchar(255), password varchar(255), fullname varchar(255), dob varchar(255), email varchar(255), phone varchar(255), address varchar(255))'
            except:
                pass
            mycursor.execute(query)
        except:
            mycursor.execute('use motorbikemanagement')
        # check if the user is already in the database
        try:
            query = 'create table user_data(username varchar(255), password varchar(255), fullname varchar(255), dob varchar(255), email varchar(255), phone varchar(255), address varchar(255))'
            mycursor.execute(query)
        except:
            pass
        query = 'select * from user_data where username = %s'
        mycursor.execute(query, username)
        result = mycursor.fetchall()
        if len(result) != 0:
            messagebox.showerror("Error", "Username already exists")
            return
        query = 'select * from user_data where email = %s'
        mycursor.execute(query, email)
        result = mycursor.fetchall()
        if len(result) != 0:
            messagebox.showerror("Error", "Email already exists")
            return
        query = 'insert into user_data(username, password, fullname, dob, email, phone, address) values(%s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(query, (username, user_password, fullname, dob, email, phone, address))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Sign up successfully")

class ForgotPass(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title("Forgot Password")
        global screen_width, screen_height
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{int(self.screen_width*3/4)}x{int(self.screen_height*3/4)}")
        self.window.configure(background="#cc0000")
        self.create_background()
        self.create_widgets()
        self.move_in()

    def create_background(self):
        frameCnt = 12
        file_name = '../img/login_page.gif'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        frames = [tk.PhotoImage(file=file_path, format=f"gif -index {i}") for i in range(frameCnt)]
        for i in range(frameCnt):
            frames[i] = frames[i].subsample(2, 2)
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            try:
                self.label.configure(image=frame)
            except:
                return
            self.window.after(100, update, ind)
        self.label = tk.Label(self.window, bg = "#cc0000")
        self.label.place(x = 400, y = 0)
        self.window.after(0, update, 0)
    
    def move_in(self):
        x = 0
        while x <= 400:
            self.label.place(x=x, y=0)
            x += 1
            self.window.update()
        self.label.place(x=400, y=0)
        self.label.after_cancel(self.update)

    def move_out(self, event, window, duration):
        try:
            if self.label.winfo_x() is None:
                return
            x = self.label.winfo_x()
            self.label.place(x=x+30)
            self.window.after(30, self.move_out, event, window, duration)
            if x > 1200:
                self.window.after(0, self.login())
        except:
            return

    def create_widgets(self):   
        #create a label to ask for the username
        self.label_username = ttk.Label(self.window, text="Username:", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_username = tk.Entry(self.window, width=32, font=("Inconsolata", 10), background="black", bd = 2, fg="black", bg= "white")

        self.label_email = ttk.Label(self.window, text="Email:", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_email = tk.Entry(self.window, width=32, font=("Inconsolata", 10), background="black", bd = 2, fg="black", bg= "white")

        #create a button to send the email
        self.button_send = tk.Button(self.window, text="Send", command = self.process_request, width=10)
        self.button_cancel = ttk.Button(self.window, text="Cancel", width=10)
        self.button_cancel.bind("<Button-1>", lambda event: self.move_out(event, self.window, 5))
        
        #pack widgets and set the position on the background
        self.label_username.place(relx=0.483, rely=0.5, anchor="e")
        self.entry_username.place(relx=0.41, rely=0.55, anchor="w")
        self.label_email.place(relx=0.4572, rely=0.6, anchor="e")
        self.entry_email.place(relx=0.41, rely=0.65, anchor="w")
        self.button_send.place(relx=0.4458, rely=0.75, anchor="center")
        self.button_cancel.place(relx=0.579, rely=0.75, anchor="center")

    def process_request(self):
        global username
        username = self.entry_username.get()
        email = self.entry_email.get()
        if username == "" or email == "":
            messagebox.showerror("Error", "something is missing")
        else:
            try:
                db = UserRestorePassword()
                if db.check_email(username, email):
                    try:                       
                        db.send_email(email)
                        messagebox.showinfo("Success", "Email sent")
                        self.create_widgets2()
                    except:
                        messagebox.showerror("Error", "Error in sending email")
                else:
                    messagebox.showerror("Error", "Email not found")
            except:
                messagebox.showerror("Error", "Error in connection")
                return

    def create_widgets2(self):
        self.entry_user = self.entry_username.get()
        self.entry_username.destroy()
        self.label_username.destroy()
        self.label_email.destroy()
        self.entry_email.destroy()
        self.button_send.destroy()
        self.button_cancel.destroy()
        # create a new label and entry to ask for the code
        self.label_code = ttk.Label(self.window, text="Code", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_code = tk.Entry(self.window, width=20, font=("Inconsolata", 10), background="black", bd = 2, fg="black", bg= "white")

        self.button_confirm = tk.Button(self.window, text="Confirm", command = self.handle_confirm, width=10)
        self.button_cancel = tk.Button(self.window, text="Cancel", command=self.login, width=10)

        self.label_code.place(relx=0.483, rely=0.5, anchor="e")
        self.entry_code.place(relx=0.45, rely=0.55, anchor="w")

        self.button_confirm.place(relx=0.4572, rely=0.65, anchor="center")
        self.button_cancel.place(relx=0.565, rely=0.65, anchor="center")

        # if the code is correct, create a new label and entry to ask for the new password
    def handle_confirm(self):
        # hash the code input by the user
        code1 = self.entry_code.get()        
        if UserRestorePassword().check_code(code1):
            self.create_widgets3()            
        else:
            messagebox.showerror("Error", "Wrong code") 

    def on_entry_focus_in(self, event, entry):
        if entry.get() == "This field is required":
            entry.delete(0, "end")
            entry.insert(0, "")
        if entry.get() == "This is not a valid email":
            entry.delete(0, "end")
            entry.insert(0, "")
        if entry.get() == "DD/MM/YYYY":
            entry.delete(0, "end")
            entry.insert(0, "")
        entry.config(background="#ffffff")
    
    def on_entry_focus_out(self, event, entry):
        if entry.get() == "":
            entry.insert(0, "This field is required")
            entry.config(background="red")

    def validate_password(self, event, entry):
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
        if (re.fullmatch(regex, entry.get())):
            entry.config(background="#ffffff")
        else:
            entry.config(background="red")
            entry.delete(0, "end")
            entry.insert(0, "Must contain at least 8 characters, 1 uppercase, 1 lowercase and 1 number and no special characters")
    
    def show_password(self, event, entry):
        if entry["show"] == "*":
            # show the password
            entry["show"] = ""
        else:
            entry["show"] = "*"

    def create_widgets3(self):
        self.label_code.destroy()
        self.entry_code.destroy()
        self.button_confirm.destroy()
        self.button_cancel.destroy()

        self.label_new_pass = ttk.Label(self.window, text="New Password:", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_new_pass = tk.Entry(self.window, show="*", width=32, font=("Inconsolata", 10), background="#f0f3f4", bd = 2)
        self.entry_new_pass.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_new_pass))
        self.entry_new_pass.bind("<FocusOut>", lambda event: self.validate_password(event, self.entry_new_pass))

        self.label_confirm_pass = ttk.Label(self.window, text="Confirm Password", font=("Inconsolata", 14), background="#cc0000", foreground= "white")
        self.entry_confirm_pass = tk.Entry(self.window, show="*", width=32, font=("Inconsolata", 10), background="#f0f3f4", bd = 2)
        self.entry_confirm_pass.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, self.entry_confirm_pass))
        self.entry_confirm_pass.bind("<FocusOut>", lambda event: self.validate_password(event, self.entry_confirm_pass))

        self.button_confirm = tk.Button(self.window, text="Confirm", command = self.handle_password, width=10)
        self.button_cancel = ttk.Button(self.window, text="Cancel", command=self.login, width=10)

        self.label_new_pass.place(relx=0.512, rely=0.5, anchor="e")
        self.entry_new_pass.place(relx=0.41, rely=0.55, anchor="w")
        self.label_confirm_pass.place(relx=0.536, rely=0.6, anchor="e")
        self.entry_confirm_pass.place(relx=0.41, rely=0.65, anchor="w")
        self.button_confirm.place(relx=0.4458, rely=0.75, anchor="center")
        self.button_cancel.place(relx=0.579, rely=0.75, anchor="center")

        # default state is hidden
        image = '../img/close_eye.png'
        #create an image object
        file_path = os.path.join(os.path.dirname(__file__), image)
        self.hide_password_icon = tk.PhotoImage(file=file_path)
        #resize the image
        self.hide_password_icon = self.hide_password_icon.subsample(10, 10)
        #create a label to display the image
        self.hide_password = tk.Button(self.window, image=self.hide_password_icon, background="#ffffff", bd = 0)
        self.hide_password.place(relx=0.6, rely=0.55, anchor="center")        
        self.hide_password.bind("<Button-1>", lambda event: self.show_password(event, self.entry_new_pass))
    
        # default state is hidden
        image1 = '../img/close_eye.png'
        #create an image object
        file_path1 = os.path.join(os.path.dirname(__file__), image1)
        self.hide_password_icon1 = tk.PhotoImage(file=file_path1)
        #resize the image
        self.hide_password_icon1 = self.hide_password_icon1.subsample(10, 10)
        #create a label to display the image
        self.hide_password1 = tk.Button(self.window, image=self.hide_password_icon1, background="#ffffff", bd = 0)
        self.hide_password1.place(relx=0.6, rely=0.65, anchor="center")
        self.hide_password1.bind("<Button-1>", lambda event: self.show_password(event, self.entry_confirm_pass))

    def handle_password(self):
        new_pass = self.entry_new_pass.get()
        confirm_pass = self.entry_confirm_pass.get()

        if new_pass == confirm_pass:
            try:
                db = UserRestorePassword()
                #hash the new password
                db.change_password(username, new_pass)
                messagebox.showinfo("Success", "Password updated successfully") 
                self.login()
            except:
                messagebox.showerror("Error", "Error in connection")
                return
        else:
            messagebox.showerror("Error", "Passwords do not match")
            return

    def login(self):
        self.destroy()
        try:
            self.entry_username.destroy()
            self.label_username.destroy()
            self.label_email.destroy()
            self.entry_email.destroy()
            self.button_send.destroy()
            self.button_cancel.destroy()
        except:
            pass
        try:
            self.label_code.destroy()
            self.entry_code.destroy()
            self.button_confirm.destroy()
            self.button_cancel.destroy()
        except:
            pass
        try:
            self.label_new_pass.destroy()
            self.entry_new_pass.destroy()
            self.label_confirm_pass.destroy()
            self.entry_confirm_pass.destroy()
            self.button_confirm.destroy()
            self.button_cancel.destroy()
        except:
            pass
        try:
            self.label.destroy()
            self.hide_password.destroy()
            self.hide_password1.destroy()
        except:
            pass
        self.window.switch_frame(LoginPage)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()