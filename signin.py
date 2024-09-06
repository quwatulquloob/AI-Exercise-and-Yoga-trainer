from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql
import subprocess
import sys
import json
import subprocess
import sys


def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='password@123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Error')
            return

        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username=%s and password=%s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row is None:
            messagebox.showerror('Error', 'Invalid Username or Password')
        else:
            messagebox.showinfo('Welcome', 'Login is Successful')
            print(f"Logged in user data: {row}")  # Print the user's data
            login_window.destroy()

            # Exclude password from user data
            user_data = {
                "id": row[0],
                "email": row[1],
                "username": row[2]
                # Add other fields as needed, but exclude the password
            }

            try:
                # Convert the user data to a JSON string and pass it as an argument
                user_data_json = json.dumps(user_data)
                subprocess.run([sys.executable, 'Gui.py', user_data_json], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running Gui.py script: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")



def on_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)

def pass_E(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0,END)
def hide():
    openeye.configure(file='images/closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)
def show():
    openeye.configure(file='images/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)
def asfi():
    login_window.destroy()
    import signup
def forget():

    def change_password():
        if U_Entry.get()==''or F_U_E.get()=='' or F_P_E.get()=='':
            messagebox.showerror('Error','Requried all Fields',parent=window)
        elif F_U_E.get()!=F_P_E.get():
            messagebox.showerror('Error', 'Password does not Match', parent=window)
        else:
            con = pymysql.connect(host='localhost', user='root', password='HF@007219',database='userdata')
            mycursor = con.cursor()
            query='select * from data where username=%s'
            mycursor.execute(query,(U_Entry.get()))
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Incorrect User Name',parent=window)
            else:
                query='update data set password=%s where username=%s'
                mycursor.execute(query,(F_U_E.get(),F_P_E.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Password is Reset,Please login with new password',
                                    parent=window)
                window.destroy()

    window=Toplevel()
    window.title('Forget Window')
    bgImage = ImageTk.PhotoImage(file='images/background.jpg')
    bgLabel = Label(window, image=bgImage)
    bgLabel.grid()

    frame = Frame(window, bg='white')
    frame.place(x=460, y=60)

    heading = Label(frame, text='Reset Password', font=('Microsoft Yauheni UI Light', 18, 'bold'), bg='white',
                    fg='firebrick1')
    heading.grid(row=0, column=0, padx=10, pady=10)

    emailLabel = Label(frame, text='Username', font=('Microsoft Yauheni UI Light', 10, 'bold'), bg='white',
                       fg='firebrick1')
    emailLabel.grid(row=1, column=0, sticky='w', padx=25, pady=(10, 0))

    U_Entry = Entry(frame, width=32, font=('Microsoft Yauheni UI Light', 10, 'bold'), fg='black', bg='yellow')
    U_Entry.grid(row=2, column=0, sticky='w', padx=25)

    usernameLabel = Label(frame, text='New_Password', font=('Microsoft Yauheni UI Light', 10, 'bold'), bg='white',
                          fg='firebrick1')

    usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))
    F_U_E = Entry(frame, width=32, font=('Microsoft Yauheni UI Light', 10, 'bold'), fg='Black', bg='yellow2')
    F_U_E.grid(row=4, column=0, sticky='w', padx=25)

    passwordLabel = Label(frame, text='Confrim Password', font=('Microsoft Yauheni UI Light', 10, 'bold'), bg='white',
                          fg='firebrick1')
    passwordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

    F_P_E = Entry(frame, width=32, font=('Microsoft Yauheni UI Light', 10, 'bold'), fg='Black', bg='yellow2')
    F_P_E.grid(row=6, column=0, sticky='w', padx=25)

    Submit = Button(frame, text='Submit', font=('open Sans', 9, 'bold'), bd=0, bg='yellow2',
                          activebackground='yellow2', activeforeground='white', width=22, padx=10, pady=10,
                          fg='black', cursor='hand2',command=change_password)
    Submit.grid(row=8, column=0, padx=10,pady=150)

    window.mainloop()
login_window=Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0,0)
login_window.title('Login Page')
bgImage=ImageTk.PhotoImage(file='images/bg.jpg')
bgLabel=Label(login_window,image=bgImage)
bgLabel.place(x=0,y=0)
heading=Label(login_window,text='USER LOGIN',font=('Microsoft Yauheni UI Light',23,'bold'),bg='white',fg='firebrick1')
heading.place(x=605,y=120)
usernameEntry=Entry(login_window,width=25,font=('Microsoft Yauheni UI Light',11,'bold'),bd=0,fg='firebrick1')
usernameEntry.place(x=580,y=200)
usernameEntry.insert(0,'Username')
usernameEntry.bind('<FocusIn>',on_enter)
Frame(login_window,width=250,height=2,bg='firebrick1').place(x=580,y=222)
passwordEntry=Entry(login_window,width=25,font=('Microsoft Yauheni UI Light',11,'bold'),bd=0,fg='firebrick1')
passwordEntry.place(x=580,y=260)
passwordEntry.insert(0,'Password')
passwordEntry.bind('<FocusIn>',pass_E)
Frame(login_window,width=250,height=2,bg='firebrick1').place(x=580,y=280)
openeye=PhotoImage(file='images/openeye.png')
eyeButton=Button(login_window,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=800,y=250)
forgetButton=Button(login_window,text='Forgot Password?',bd=0,bg='white',activebackground='white',cursor='hand2',font=('Microsoft Yauheni UI Light',9,'bold'),fg='firebrick1',
                    activeforeground='firebrick1',command=forget)
forgetButton.place(x=715,y=295)

loginButton=Button(login_window,text='LOGIN',font=('Open Sans',14,'bold'),fg='white',bg='firebrick1',activeforeground='white',activebackground='firebrick1',cursor='hand2',
                   bd=0,width=19,command=login_user)
loginButton.place(x=578,y=350)

orLable=Label(login_window,text='-------------OR-------------',font=('Open sans',16),fg='firebrick1',bd=0,bg='white')
orLable.place(x=585,y=400)

facebook_logo=PhotoImage(file='')
fbLabel=Label(login_window,image=facebook_logo,bd=0,bg='white')
fbLabel.place(x=640,y=440)

T_logo=PhotoImage(file='')
T_Label=Label(login_window,image=T_logo,bd=0,bg='white')
T_Label.place(x=690,y=440)

G_logo=PhotoImage(file='')
GLabel=Label(login_window,image=G_logo,bd=0,bg='white')
GLabel.place(x=740,y=440)

orLable=Label(login_window,text='Do you already have an account?',font=('Open sans',9,'bold'),fg='firebrick1',
              bd=0,bg='white')
orLable.place(x=575,y=450)

CreatButton=Button(login_window,text='Create new account',font=('Open Sans',9,'bold underline'),fg='blue',bg='white',activeforeground='blue',activebackground='white',cursor='hand2',
                   bd=0,command=asfi)
CreatButton.place(x=695,y=485)

login_window.mainloop()

