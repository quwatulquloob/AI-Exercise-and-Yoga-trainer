from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql

signup_window=Tk()
signup_window.title('Signup Page')
signup_window.resizable(False,False)
background=ImageTk.PhotoImage(file='images/bg.jpg')
bglabel=Label(signup_window,image=background)
bglabel.grid()
frame=Frame(signup_window,bg='white')
frame.place(x=554,y=100)

def clear():
    emailEntry.delete(0,END)
    U_E.delete(0,END)
    P_E.delete(0,END)
    C_P_E.delete(0,END)
    check.set(0)

def connect_database():
    if emailEntry.get()=='' or U_E.get()=='' or P_E.get()=='' or C_P_E.get()=='':
        messagebox.showerror('Error','All Fields Are Required')
    elif P_E.get()!=C_P_E.get():
        messagebox.showerror('Error', 'Password Missed Match')
    elif check.get()==0:
        messagebox.showerror('Error','Please accept Terms and Conditions')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='password@123')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Database connectivity Error Please check')
            return
        try:
            query='create database userdata'
            mycursor.execute(query)
            query='use userdata'
            mycursor.execute(query)
            # query='create table data(id int auto_increment primary key not null, email varchar(50),' \
            #       'username varchar(100),password varchar(20),secore int(500) primary key not null)'
            query = 'create table data(id int auto_increment primary key not null, email varchar(50),username varchar(100),password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')
            query='select * from data where username=%s'
            mycursor.execute(query,(U_E.get()))
            userrow=mycursor.fetchone()
            if userrow !=None:
                messagebox.showerror('Error','User already Register try other Email')
            else:
                query='insert into data(email,username,password) values (%s,%s,%s)'
                mycursor.execute(query,(emailEntry.get(),U_E.get(),P_E.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Registration Is successful')
                clear()
                signup_window.destroy()
                import signin

def login_page():
    signup_window.destroy()
    import signin


heading=Label(frame,text='Create An Account',font=('Microsoft Yauheni UI Light',18,'bold'),bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)

emailLabel=Label(frame,text='Email',font=('Microsoft Yauheni UI Light',10,'bold'),bg='white',fg='firebrick1')
emailLabel.grid(row=1,column=0,sticky='w',padx=25,pady=(10,0))
emailEntry=Entry(frame,width=32,font=('Microsoft Yauheni UI Light',10,'bold'),fg='white',bg='firebrick1')
emailEntry.grid(row=2,column=0,sticky='w',padx=25)

usernameLabel=Label(frame,text='User_Name',font=('Microsoft Yauheni UI Light',10,'bold'),bg='white',fg='firebrick1')
usernameLabel.grid(row=3,column=0,sticky='w',padx=25,pady=(10,0))
U_E=Entry(frame,width=32,font=('Microsoft Yauheni UI Light',10,'bold'),fg='white',bg='firebrick1')
U_E.grid(row=4,column=0,sticky='w',padx=25)

passwordLabel=Label(frame,text='Password',font=('Microsoft Yauheni UI Light',10,'bold'),bg='white',fg='firebrick1')
passwordLabel.grid(row=5,column=0,sticky='w',padx=25,pady=(10,0))
P_E=Entry(frame,width=32,font=('Microsoft Yauheni UI Light',10,'bold'),fg='white',bg='firebrick1')
P_E.grid(row=6,column=0,sticky='w',padx=25)

C_PLabel=Label(frame,text='Confirmed Password',font=('Microsoft Yauheni UI Light',10,'bold'),bg='white',fg='firebrick1')
C_PLabel.grid(row=7,column=0,sticky='w',padx=25,pady=(10,0))
C_P_E=Entry(frame,width=32,font=('Microsoft Yauheni UI Light',10,'bold'),fg='white',bg='firebrick1')
C_P_E.grid(row=8,column=0,sticky='w',padx=25)

check=IntVar()

termsandconditions=Checkbutton(frame,text='I agree to the Terms & Conditions',font=('Microsoft Yauheni UI Light',9,'bold'),fg='firebrick1',bg='white',activebackground='white',activeforeground='firebrick1',
                               cursor='hand2',variable=check)
termsandconditions.grid(row=9,column=0,pady=10,padx=15)

signupButton=Button(frame,text='SignUp',font=('open Sans',9,'bold'),bd=0,bg='firebrick1',
                    activebackground='firebrick1',activeforeground='white',width=17,padx=10,pady=10,fg='white',cursor='hand2',
                    command=connect_database)
signupButton.grid(row=10,column=0)

Allready=Label(frame,text='Already Have An Account?',font=('open Sans',9,'bold'),fg='firebrick1',bd=0,bg='white')
Allready.grid(row=11,column=0,sticky='w',padx=10,pady=10)

loginButton=Button(frame,text='Sign in',font=('Open Sans',9,'bold underline'),fg='blue',bg='white',activeforeground='blue',activebackground='white',cursor='hand2',
                   bd=0,command=login_page)
loginButton.grid(row=12,column=0)

signup_window.mainloop()


