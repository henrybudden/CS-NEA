from tkinter import *
import sqlite3
import matplotlib.pyplot as plt
 

attempts = 0

def login_check(): #Allows logins for registered users and checks admin privilages
    global attempts
    username = username_box.get()
    password = password_box.get()

    try:
        with sqlite3.connect("logins.db") as db:
            cursor = db.cursor()
            cursor.execute("select passwd from data where username=?", (username,))
            real_password = cursor.fetchone()
        if password == real_password[0]:
            print("Login Allowed")
            attempts = 0
            with sqlite3.connect("logins.db") as db:
                cursor = db.cursor()
                cursor.execute("select admin from data where username=?", (username,))
                admin = cursor.fetchone()
            if admin[0] == 1:  #If user is admin
                admin_screen.tkraise()
                graph()
            else:  
                non_admin_screen.tkraise()
        else:
            if attempts == 3:
                root.destroy()
            warning = "Login Failed - Incorrect Password. You have "+str(3 - attempts)+ " attempts remaining."
            messagebox.showerror('OK', warning)
            attempts += 1
            logout() 
    except:
            if attempts == 3:
                root.destroy()
            warning = "Login Failed - Incorrect Username. You have "+str(3 - attempts)+ " attempts remaining."
            messagebox.showerror('OK', warning)
            attempts += 1
            logout()

def logout(): #Returns to login screen and clears login boxes
    print("Get lost")
    password_box.delete(0, END)
    username_box.delete(0, END)
    login_screen.tkraise()

def register_new_user_screen(): #Raise registration screen
    registration_screen.tkraise()

def registration(): #Registers a new user and adds to database
    username = new_username_box.get()
    password = new_password_box.get()
    password2 = new_password2_box.get()
    if password != password2:   #If double entry validation fails
        warning = "Registration Failed - Passwords do not Match. \nPlease try again."
        messagebox.showerror('OK', warning)
        new_password2_box.delete(0, END)
        new_password_box.delete(0, END)
    else:
        values = (username, password, "0")
        with sqlite3.connect("logins.db") as db:
            cursor = db.cursor()
            sql = "insert into data (username, passwd, admin) values (?,?,?)"
            cursor.execute(sql, values)
            db.commit()
        info = "Registration Successful"
        messagebox.showinfo('OK', info)
        logout()

def graph():
    users = []
    values = []
    
    with sqlite3.connect("logins.db") as db:
        cursor = db.cursor()
        cursor.execute("select user, sum(SaleValue) from Sales GROUP BY user")
        SaleValues = cursor.fetchall()
        for totals in SaleValues:
            users.append(totals[0])
            values.append(totals[1])
    # Data to plot
    labels = users
    sizes = values
    colors = ['gold', 'yellowgreen']
    explode = (0, 0)  # explode 1st slice
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
     
    plt.axis('equal')
    plt.show()
    
root = Tk()
root.title("Login")
root.minsize(200,255)
login_screen = Frame(root)
login_screen.grid(column=0, row=0, sticky=NE+SW)

username = Label(login_screen,
              fg = "black",
              font = "Calibri 14 bold",
              text  = "Username:")
username.pack()
username_box = Entry(login_screen)
username_box.pack()
password = Label(login_screen,
              fg = "black",
              font = "Calibri 14 bold",
              text  = "Password:")
password.pack()
password_box = Entry(login_screen, show = "*")
password_box.pack()
registration_button = Button(login_screen,
                     font = "Calibri 14",
                     text = "Register New User",
                     command = register_new_user_screen)
registration_button.pack(side = BOTTOM)
login_button = Button(login_screen,
                     font = "Calibri 14",
                     text = "Login",
                     command = login_check)
login_button.pack(side = BOTTOM)


non_admin_screen = Frame(root)
non_admin_screen.grid(column=0, row=0, sticky=NE+SW)

message = Label(non_admin_screen,
                     fg = "black",
                     font = "Calibri 14 italic",
                     text = "Non Admin Screen")
message.pack()
logout_button = Button(non_admin_screen,
                           font = "Calibri 14",
                           text = "Log Off",
                           command = logout)
logout_button.pack(side = BOTTOM)


admin_screen = Frame(root)
admin_screen.grid(column=3, row=3, sticky=NW+SE)

message = Label(admin_screen,
                     fg = "black",
                     font = "Calibri 14 italic",
                     text = "Admin Screen")
message.pack()
logout_button = Button(admin_screen,
                           font = "Calibri 14",
                           text = "Log Off",
                           command = logout)
logout_button.pack(side = BOTTOM)


registration_screen = Frame(root)
registration_screen.grid(column=0, row=0, sticky=NW+SE)

message = Label(registration_screen,
                     fg = "black",
                     font = "Calibri 14 italic",
                     text = "Registration Screen")
message.pack()
new_username = Label(registration_screen,
              fg = "black",
              font = "Calibri 14 bold",
              text  = "Enter New Username:")
new_username.pack()
new_username_box = Entry(registration_screen)
new_username_box.pack()
new_password = Label(registration_screen,
              fg = "black",
              font = "Calibri 14 bold",
              text  = "Enter New Password:")
new_password.pack()
new_password_box = Entry(registration_screen, show = "*")
new_password_box.pack()
new_password2 = Label(registration_screen,
              fg = "black",
              font = "Calibri 14 bold",
              text  = "Re-enter New Password:")
new_password2.pack()
new_password2_box = Entry(registration_screen, show = "*")
new_password2_box.pack()
save_button = Button(registration_screen,
                           font = "Calibri 14",
                           text = "Save and Exit",
                           command = registration)
save_button.pack(side = BOTTOM)


login_screen.tkraise()
root.mainloop()

