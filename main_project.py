import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import ssl
from tkinter import END, StringVar, Text, Tk,Label,Frame,Entry,Button, Toplevel,messagebox,filedialog                        #import root window class    
import os,shutil
from tkinter import Checkbutton,IntVar,DISABLED,NORMAL
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox                                #impor from tkinter module combobox
import time                                                     #import time
from PIL import Image,ImageTk                                   #import image from Pillow libs
import random
import bank_projec_tables
import sqlite3
import smtplib
from email.message import EmailMessage
import bank_project_mails
import project_mails_pdf
from tkinter import messagebox
from datetime import datetime
import csv
from logging import root


def open_help_desk():
    help_win = Toplevel(root)
    help_win.title("Help Desk - Contact Us")
    help_win.geometry("400x400")

    Label(help_win, text="Contact Help Desk", font=('arial',16,'bold')).pack(pady=10)

    Label(help_win, text="Name:", font=('arial',12)).pack()
    name_entry = Entry(help_win, font=('arial',12))
    name_entry.pack()

    Label(help_win, text="Email:", font=('arial',12)).pack()
    email_entry = Entry(help_win, font=('arial',12))
    email_entry.pack()

    Label(help_win, text="Message:", font=('arial',12)).pack()
    message_entry = Text(help_win, height=5, font=('arial',12))
    message_entry.pack()

    def submit_help():
        name = name_entry.get()
        email = email_entry.get()
        message = message_entry.get("1.0", END).strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("help_requests.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, name, email, message])
        
        messagebox.showinfo("Submitted", "Your help request has been submitted.")
        help_win.destroy()

    Button(help_win, text="Submit", font=('arial',12,'bold'), bg="lightgreen", command=submit_help).pack(pady=10)

def generate_captcha():                                         #Make function to generate captcha 
    captcha=[]
    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c)

        n=random.randint(0,9)
        captcha.append(str(n))

    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh():
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)

def scroll_header():
    global header_text
    header_text = header_text[1:] + header_text[0]  # Rotate left
    header_lbl.config(text=header_text)
    root.after(220, scroll_header)


def scroll_text():                                                      #This function help to footer scroll
    global scrolling_text
    scrolling_text = scrolling_text[1:] + scrolling_text[0]             # Rotate text left
    footer_lbl.config(text=scrolling_text)
    root.after(220, scroll_text)

def update_datetime():
    current_time = time.strftime("%A, %d %B %Y | %I:%M:%S %p")
    datetime_lbl.config(text=current_time)
    root.after(1000, update_datetime)

def animate_left():
    logo_anmi.config(image=img_list[left_index[0]])
    left_index[0] = (left_index[0] + 1) % len(img_list)
    root.after(2000, animate_left)

def animate_right():
    logo_lbl.config(image=img_list[right_index[0]])
    right_index[0] = (right_index[0] + 1) % len(img_list)
    root.after(1500, animate_right)


root=Tk()                                                       #root window object
root.state("zoomed")                                            #root window max size
root.configure(bg='light yellow')                                       #root window colour
root.title("KBC Bank")                                          #root window title decide
root.resizable(width=False,height=False)                        #root window does not resize

title_lbl=Label(root,text="Banking Automation",bg="light yellow",font=("revenue",50,"bold","underline"),fg='red')     #labeling of root window
title_lbl.pack()                                                #window top center show

# today_lbl=title=Label(root,text=time.strftime("%A,%d %B %Y"),bg="light yellow",font=("arial",13,"bold"),fg='brown')       #labeling of time
# today_lbl.pack(pady=10)

# time_lbl = Label(root,bg="light yellow", font=("arial", 14, "bold"), fg='blue')
# time_lbl.place(relx=.46,rely=.18)

# Combined label for date + live time
datetime_lbl = Label(root, bg="light yellow", font=("arial", 13, "bold"), fg='blue')
datetime_lbl.place(relx=.36, rely=.13)


img_list=[ImageTk.PhotoImage(Image.open("images/rbi.jpg").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/banking.jpg").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/bankk.png").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/banks.jpg").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/bnk.png").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/bks.jpg").resize((220, 150)), master=root),
        ImageTk.PhotoImage(Image.open("images/bkk.jpg").resize((220, 150)), master=root)]

# Left animated logo
logo_anmi =Label(root, bg='white')
logo_anmi.place(relx=0, rely=0)

# Right animated logo
logo_lbl = Label(root, bg='white')
logo_lbl.place(relx=0.82, rely=0)

# Animation control
left_index = [1] 
right_index =[0]

# img=Image.open("rbi.jpg").resize((220,150))                 #root window image add and resizing
# img_bitmap=ImageTk.PhotoImage(img,master=root)              #change image jpg to Bitmap

# logo_lbl=Label(root,image=img_bitmap)                       #label of image in root window
# logo_lbl.place(relx=0,rely=0)                               #postion of logo in root window

# img1=Image.open("banking.jpg").resize((220,150))            #root window image add and resizing
# img1_bitmap=ImageTk.PhotoImage(img1,master=root)            #change image jpg to Bitmap

# logo_lbl=Label(root,image=img1_bitmap)                      #label of image in root window
# logo_lbl.place(relx=.82,rely=0)                             #positioning of image


# Set the header text message
header_text = "  !! Home loan at low interest rate /  Easy to Investment on mutual account !!     "

# Header Label (top of window)
header_lbl =Label(root, text=header_text, bg='light yellow', fg='brown', font=('georgia', 15, 'bold'))
header_lbl.pack(side='top', pady=30)


scrolling_text="  Laxmi cheat and fund...21 Din mein Paise Double  "
footer_lbl=Label(root,text="scrolling_text",bg='light yellow',fg='blue',font=('georgia',12,'bold'))               #footer of the root window
footer_lbl.pack(side='bottom',pady=12)                      #footer and pack of side bottom

def main_screen():
    def login():                                                        #This function help to login Button works
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget("text")
        actual_cap=actual_cap.replace(' ','')
    
        if utype=="Admin":
            if uacn=='0' and upass=="admin":
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid Captcha')
            else:
                messagebox.showerror('Login','Invalid ACN/PASS/TYPE')
        elif utype=="User":                                                             #comobobox select user compulsory
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("User Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(uacn)
            else:
                messagebox.showerror('Login','Invalid Captcha')
        else:
            messagebox.showerror("Login","Kindly select Valid user Type")

    frm=Frame(root)                                                                     #frame configuration
    frm.configure(bg='sky blue')
    frm.place(relx=0,rely=.23,relwidth=1,relheight=.71)

    user_lbl=Label(frm,text="User Type",bg='sky blue',font=('arial',16,'bold'))            #Create user type in the combobox
    user_lbl.place(relx=.33,rely=.1)

    user_combo=Combobox(frm,values=['Admin','User','---Select---'],font=('cambria',16),state='readonly')                #create combobox and fill the details
    user_combo.current(2)                                                                                               #Default value of combobox
    user_combo.place(relx=.48,rely=.1)

    acn_label=Label(frm,text="Account No.",bg='sky blue',font=('arial',16,'bold'))                      #Create ACN of user
    acn_label.place(relx=.33,rely=.21)
    
    acn_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  #Entry field of user ACN
    acn_entry.place(relx=.48,rely=.21)
    acn_entry.focus()

    pass_label=Label(frm,text="Password",bg='sky blue',font=('arial',16,'bold'))                        #Create Password of user
    pass_label.place(relx=.33,rely=.32)

    pass_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink',show='*')                                                  #Entry field of user Password
    pass_entry.place(relx=.48,rely=.32)
   
    show_password = IntVar()                                                        #Module of TKinter
    def password():                                                                     #Define a function to show password
        if show_password.get():
            pass_entry.config(show='')
        else:
            pass_entry.config(show='*')

    show_password_label= Checkbutton(frm, text="Show Password", variable=show_password,bg='sky blue', font=('arial', 12), command=password)               #Entry field of show password and button works
    show_password_label.place(relx=0.48, rely=0.4) 

    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg='white',font=('arial',16,'bold'))                #Show and call the captcha from def function line no.9
    captcha_lbl.place(relx=.48,rely=.48)                                                              #Place The captcha field

    refresh_btn=Button(frm,text="refresh",fg="blue",font=('arial',8,'bold'),bd=5,command=refresh)           #Refresh Button to captcha
    refresh_btn.place(relx=.6,rely=.48)                                                                     #place the refresh button

    inputcap_label=Label(frm,text="Captcha",bg='sky blue',font=('arial',16,'bold'))                      #Create Captcha of user
    inputcap_label.place(relx=.33,rely=.58)                                                              #Place the Captcha in the frame
    
    inputcap_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink')                                   #Entry field of user Captcha
    inputcap_entry.place(relx=.48,rely=.58)                                                             #place the entry field of user captch              

    login_btn=Button(frm,text="login",bg="powder blue",fg="green",font=('arial',14,'bold'),bd=5,command=login)            #create login Button
    login_btn.place(relx=.5,rely=.7)                                                                        #place the login button

    def reset():
        inputcap_entry.delete(0,"end")
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        user_combo.current(2)
        user_combo.focus()
        
    reset_btn=Button(frm,text="reset",bg="powder blue",fg="blue",font=('arial',14,'bold'),bd=5,command=reset)             #create the reset button
    reset_btn.place(relx=.58,rely=.7)                                                                       #place the reset button in the frame

    forgot_btn=Button(frm,width=18,text="forget password",bg="powder blue",fg="red",font=('arial',14,'bold'),bd=5,command=forgot_screen)              #create forget password button
    forgot_btn.place(relx=.48,rely=.82)                                                                                         #place the forget button in then frame
    
    global help_btn
    help_btn = Button(frm, width=9, text="Help Desk", bg="orange", fg="black", font=('arial',9,'bold'), bd=5,command=open_help_desk)                 #create the help desk button
    help_btn.place(relx=.92, rely=.9)                                                                                          #place the help desk button in the frame

def admin_screen():                                                                 #admin screen function when admin login
    def next_frame():
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            ugender=gender_combo.get()
            udob=DOB_entry.get()
            uaddress=add_entry.get()
            uadhar=adhar_entry.get()
            unomainee=nomainee_entry.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d %B %Y")
            upass=generate_captcha().replace(' ','')
            uifsc_Code="Moon98911"
            try:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                
                query='insert into accounts values(null,?,?,?,?,?,?,?,?,?,?,?,?)'
                curobj.execute(query,(uname,upass,uemail,umob,udob,uaddress,uadhar,unomainee,ugender,uifsc_Code,uopendate,ubal))
                conobj.commit()
                conobj.close()

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                
                query="select max(accounts_acno) from accounts"
                curobj.execute(query)
                uacno=curobj.fetchone()[0]
            except Exception as db_err:
                messagebox.showerror("Open Account",f"Database error :{db_err}")
            finally:
                conobj.close()
            
            try:
                project_mails_pdf.send_mail_for_openac_pdf(uemail,uacno,uname,udob,upass,uifsc_Code,uopendate,umob,ubal,uaddress)
                msg=f'Account opened with ACN {uacno} and mail sent to {uemail}, Kindly check your spam also'
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)
            
        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            DOB_entry.delete(0,"end")
            add_entry.delete(0,"end")
            adhar_entry.delete(0,"end")
            nomainee_entry.delete(0,"end")
            gender_combo.current(3)
            name_entry.focus()

        for widget in frm.winfo_children():
            widget.destroy()

        nxt_frm = Frame(frm,highlightthickness=2, highlightbackground='black', bg='white')
        nxt_frm.place(relx=.22, rely=.09, relwidth=.75, relheight=.78)

        Label(nxt_frm, text="This is open account screen", font=('arial', 16, 'bold'), fg='green', bg='white').pack(pady=10)

        name_lbl=Label(nxt_frm,text="Name",bg='white',font=('arial',16,'bold'))                                     #this is admin screen details to open a a/c                 
        name_lbl.place(relx=.07,rely=.1)
        
        name_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        name_entry.place(relx=.07,rely=.19)
        name_entry.focus()

        email_lbl=Label(nxt_frm,text="Email",bg='white',font=('arial',16,'bold'))                      #Create ACN of user
        email_lbl.place(relx=.07,rely=.3)
    
        email_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  #Entry field of user ACN
        email_entry.place(relx=.07,rely=.39)

        mob_lbl=Label(nxt_frm,text="Mob",bg='white',font=('arial',16,'bold'))                     
        mob_lbl.place(relx=.07,rely=.5)
        
        mob_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        mob_entry.place(relx=.07,rely=.59)

        DOB_lbl=Label(nxt_frm,text="DOB",bg='white',font=('arial',16,'bold'))                     
        DOB_lbl.place(relx=.07,rely=.7)
        
        DOB_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        DOB_entry.place(relx=.07,rely=.79)
    
        add_lbl=Label(nxt_frm,text="Address",bg='white',font=('arial',16,'bold'))                     
        add_lbl.place(relx=.65,rely=.1)
        
        add_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        add_entry.place(relx=.65,rely=.19)
        
        adhar_lbl=Label(nxt_frm,text="Adhar",bg='white',font=('arial',16,'bold'))                      #Create ACN of user
        adhar_lbl.place(relx=.65,rely=.3)
    
        adhar_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  #Entry field of user ACN
        adhar_entry.place(relx=.65,rely=.39)

        nomainee_lbl=Label(nxt_frm,text="Nomaniee",bg='white',font=('arial',16,'bold'))                     
        nomainee_lbl.place(relx=.65,rely=.5)
        
        nomainee_entry=Entry(nxt_frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        nomainee_entry.place(relx=.65,rely=.59)

        gender_lbl=Label(nxt_frm,text="Gender",bg='white',font=('arial',16,'bold'))                     
        gender_lbl.place(relx=.65,rely=.7)

        gender_combo=Combobox(nxt_frm,values=['Male','Female','Others','---Select---'],font=('cambria',16),state='readonly')                #create combobox and fill the details
        gender_combo.current(3)                                                                                               #Default value of combobox
        gender_combo.place(relx=.65,rely=.79)
       
        open_btn=Button(nxt_frm, text="Open A/c", font=('arial', 14, 'bold'), bg='lightgreen', fg='black',command=open_acn_db)
        open_btn.place(relx=.39,rely=.85)

        reset_btn=Button(nxt_frm,command=reset,text="Reset", font=('arial', 14, 'bold'), bg='lightgreen', fg='black')
        reset_btn.place(relx=.54,rely=.85)

        back_btn=Button(frm,width=7,text="back",bg="grey",fg="white",font=('arial',12,'bold'),bd=5,command=back)                #back button           
        back_btn.place(relx=.02,rely=.9)

        # logout_btn=Button(frm,width=7,text="logout",bg="grey",fg="white",font=('arial',12,'bold'),bd=5,command=logout)              #logout button to the admin
        # logout_btn.place(relx=.03,rely=.84)

    def back():                                                                             #back button function
        frm.destroy()
        admin_screen()
        

    def open_acn():                                                                  #open acount inner frame frunction
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.22,rely=.09,relwidth=.75,relheight=.78)

        #title_lbl=Label(ifrm,text="This is open account screen",bg='white',font=('arial',16,'bold'),fg='purple')                    #place the title of open account frame
        #title_lbl.pack()    
        
        doc_lbl=Label(ifrm, text="Required Documents to Open an Account:", font=('arial', 14, 'bold'), bg='white', fg='Red')
        doc_lbl.pack()
        doc_texts = [
        "i   Aadhar Card (Photocopy)",
        "ii  PAN Card (Photocopy)",
        "iii Passport-size Photograph",
        "iv  Address Proof (Electricity Bill, Rental Agreement etc.)"
        ]
        start_y=0.15
        for doc in doc_texts:
            doc_text=Label(ifrm, text=doc, font=('arial', 13), bg='white', anchor='w')
            doc_text.place(relx=.1,rely=start_y)
            start_y +=0.07

        okk_btn=Button(ifrm, text="OK", font=('arial', 14, 'bold'), bg='lightgreen', fg='black', command=next_frame)
        okk_btn.place(relx=.4,rely=.6)

    
    otp_timer = None
    countdown = 30  # seconds
    current_otp = None

    def delete_acn():                                               # Delete account inner frame function
        global otp_btn, delete_entry, timer_lbl, countdown, otp_timer, otp_display_lbl, otp_entry, verify_btn, current_otp

        def send_otp():
            global current_otp, countdown, otp_timer
            uacn=delete_entry.get()
            

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete Account","Record not found")
            else:
                otp=random.randint(100000,999999)
                current_otp=str(otp)

                bank_project_mails.send_otp(tup[3],tup[1], uacn, otp)
                messagebox.showinfo('Delete Account','OTP sent to registered mail id')

                otp_display_lbl.config(text="OTP sent")
                otp_btn.config(state=DISABLED)
                countdown = 30
                update_timer()

        def update_timer():
            global countdown, otp_timer, current_otp

            if countdown > 0:
                timer_lbl.config(text=f"Resend OTP in {countdown} sec")
                countdown -= 1
                otp_timer = timer_lbl.after(1000, update_timer)
            else:
                timer_lbl.config(text="OTP expired. Please resend.")
                current_otp = None  # Invalidate OTP
                otp_btn.config(state=NORMAL)
          
        def verify():
            uotp = otp_entry.get()
            uacn = delete_entry.get()

            if current_otp is None:
                messagebox.showerror("Delete Account", "OTP expired. Please resend.")
                return
            
            if uotp == current_otp:
                resp = messagebox.askyesno("Delete Account", "Do you want to delete this account?")

                if resp:
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'delete from accounts where accounts_acno=?'
                    curobj.execute(query, (uacn,))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Delete Account", "Account deleted successfully.")
                    frm.destroy()
                    admin_screen()

                else:
                    messagebox.showerror("Delete Account", "Incorrect OTP")

    # Frame setup
        ifrm = Frame(frm, highlightthickness=2, highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.22, rely=.09, relwidth=.75, relheight=.78)

        title_lbl = Label(ifrm, text="This is delete account screen", bg='white',font=('arial', 16, 'bold'), fg='purple')
        title_lbl.pack()

        delete_label = Label(ifrm, text="Account No.", bg='white', font=('arial', 16, 'bold'))
        delete_label.place(relx=.25, rely=.15)

        delete_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        delete_entry.place(relx=.46, rely=.15)
        delete_entry.focus()

    # Send OTP button
        otp_btn = Button(ifrm, text="Send OTP", bg="powder blue", fg="green",font=('arial', 14, 'bold'), bd=5, command=send_otp)
        otp_btn.place(relx=.25, rely=.3)

        otp_display_lbl = Label(ifrm, text="", bg='white', fg='blue', font=('arial', 14, 'bold'))
        otp_display_lbl.place(relx=0.25, rely=0.42)

        # Timer label to show countdown
        timer_lbl = Label(ifrm, text="", bg='white', font=('arial', 12))
        timer_lbl.place(relx=.25, rely=.48)

        otp_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        otp_entry.place(relx=.46, rely=.3)

        # ok_btn=Button(ifrm, text="OK", font=('arial', 14, 'bold'), bg='lightgreen', fg='black')
        # ok_btn.place(relx=.55,rely=.45)

        verify_btn = Button(ifrm, command=verify, text='Verify', bg="powder blue", fg="green", font=('arial', 14, 'bold'), bd=5)
        verify_btn.place(relx=.5, rely=.55)




    # Button outside the frame to open the account info screen
        #open_btn = Button(frm, text="Open Account", bg="yellow", fg="black", font=('arial', 16, 'bold'), bd=5, command=open_acn)              
        #open_btn.place(relx=.03, rely=.1)

    def view_acn():                                                                       #view account inner frame function
        def view_details():
            uacn=acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("View Account","Record not found")
            else:
                name_val_lbl.config(text=tup[1])
                bal_val_lbl.config(text=str(tup[12]))
                date_val_lbl.config(text=str(tup[11]))
                email_val_lbl.config(text=tup[3])
                mob_val_lbl.config(text=tup[4])

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.22,rely=.09,relwidth=.75,relheight=.78)

        title_lbl=Label(ifrm,text="This is view account screen",bg='white',font=('arial',16,'bold'),fg='purple')                        #place the title of view account frame
        title_lbl.pack()

        acn_label=Label(frm,text="Account No.",bg='white',font=('arial',16,'bold'))                                     #This is view a/c label                    
        acn_label.place(relx=.4,rely=.2)
        
        acn_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        acn_entry.place(relx=.55,rely=.2)
        acn_entry.focus()

        view_btn = Button(ifrm,command=view_details,text="View", bg="powder blue", fg="green",font=('arial', 14, 'bold'), bd=5)
        view_btn.place(relx=.55, rely=.3)

        Label(ifrm, text="User Name:", font=('arial', 14), bg='white').place(relx=0.05, rely=0.45)
        name_val_lbl = Label(ifrm, text="", font=('arial', 14, 'bold'), bg='white', fg='green')
        name_val_lbl.place(relx=0.35, rely=0.45)

        Label(ifrm, text="Available Balance:", font=('arial', 14), bg='white').place(relx=0.05, rely=0.55)
        bal_val_lbl = Label(ifrm, text="", font=('arial', 14, 'bold'), bg='white', fg='green')
        bal_val_lbl.place(relx=0.35, rely=0.55)

        Label(ifrm, text="Account Open Date:", font=('arial', 14), bg='white').place(relx=0.05, rely=0.65)
        date_val_lbl = Label(ifrm, text="", font=('arial', 14, 'bold'), bg='white', fg='green')
        date_val_lbl.place(relx=0.35, rely=0.65)

        Label(ifrm, text="Email:", font=('arial', 14), bg='white').place(relx=0.05, rely=0.75)
        email_val_lbl = Label(ifrm, text="", font=('arial', 14, 'bold'), bg='white', fg='green')
        email_val_lbl.place(relx=0.35, rely=0.75)

        Label(ifrm, text="Mobile No:", font=('arial', 14), bg='white').place(relx=0.05, rely=0.85)
        mob_val_lbl = Label(ifrm, text="", font=('arial', 14, 'bold'), bg='white', fg='green')
        mob_val_lbl.place(relx=0.35, rely=0.85)
            
    def logout():                                                                                       #logout button                                                  #function to logout button works
        resp=messagebox.askyesno("logout","Do want to Logout?")
        if resp:
            frm.destroy()
            main_screen()

    frm=Frame(root)
    frm.configure(bg='sky blue')
    frm.place(relx=0,rely=.23,relwidth=1,relheight=.71)

    wel_label=Label(frm,text="Welcome, Admin",bg='sky blue',font=('arial',16,'bold'),fg='dark blue')                      #welcom admin mssg show
    wel_label.place(relx=.0,rely=.0)

    logout_btn=Button(frm,width=7,text="logout",bg="grey",fg="white",font=('arial',12,'bold'),bd=5,command=logout)              #logout button to the admin
    logout_btn.place(relx=.03,rely=.84)
    
    open_btn=Button(frm,width=13,text="Open Account",bg="yellow",fg="black",font=('arial',16,'bold'),bd=5,command=open_acn)              #open button to the admin
    open_btn.place(relx=.03,rely=.1)

    delete_btn=Button(frm,width=13,text="Delete Account",bg="Red",fg="light yellow",font=('arial',16,'bold'),bd=5,command=delete_acn)              #delete button to the admin
    delete_btn.place(relx=.03,rely=.25)

    view_btn=Button(frm,width=13,text="View Account",bg="green",fg="white",font=('arial',16,'bold'),bd=5,command=view_acn)              #view button to the admin
    view_btn.place(relx=.03,rely=.41)

otp_timer = None
countdown = 30  # seconds
current_otp = None

def forgot_screen():                                                                    #forgot screen function
    global frm,current_otp, countdown, otp_timer
    def back():                                                                             #back button function
        frm.destroy()
        main_screen()

    def send_otp():
        global otp_timer, current_otp, countdown,tup
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()

        ucaptcha=inputcap_entry.get()
        if ucaptcha!=forgot_captcha.replace(' ',''):
            messagebox.showerror('Forgot password','Invalid captcha')
            return
        
        #authenticate acn & email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))

        tup=curobj.fetchone()
        conobj.close()
        if tup is None:
            messagebox.showerror("Forgot password","Record not found")
        else:
            otp=random.randint(100000,999999)
            current_otp = str(otp)
            bank_project_mails.send_otp(uemail,tup[1], uacn, otp)
            messagebox.showinfo('Forgot pass','OTP sent to given/registered mail id')
    
            if otp_timer is not None:
                timer_lbl.after_cancel(otp_timer)
                otp_timer = None
            countdown = 30
            resend_btn.config(state=DISABLED)
            update_timer()

            otp_entry.place(relx=.48,rely=.6)                                                             #place the entry field of user captch              
            verify_btn.place(relx=.55, rely=.75)

    def verify():
        uotp = otp_entry.get()
        if current_otp is None:
            messagebox.showerror("Forgot Password", "OTP expired. Please resend.")
            return
        if uotp == current_otp:
            messagebox.showinfo("Forgot Password", f"Your password: {tup[2]}")
        else:
            messagebox.showerror("Forgot Password","Incorrect OTP")

    def update_timer():
        global countdown, otp_timer, current_otp
        if countdown > 0:
            timer_lbl.config(text=f"Resend OTP in {countdown} sec")
            countdown -= 1
            otp_timer = timer_lbl.after(1000, update_timer)
        else:
            timer_lbl.config(text="OTP expired. Please resend.")
            current_otp = None
            resend_btn.config(state=NORMAL)
        
    # otp_entry = Entry(frm, font=('arial', 16, 'bold'), bd=5, bg='pink')
    # verify_btn = Button(frm, command=verify, text='Verify', bg="powder blue", fg="green", font=('arial', 14, 'bold'), bd=5)

    # timer_lbl = Label(frm, text="", bg='white', font=('arial', 12))
    # timer_lbl.place(relx=0.35, rely=0.67)

    # resend_btn = Button(frm, text="Resend OTP", font=('arial', 14, 'bold'), bg='orange', fg='white', bd=5, command=send_otp)
    # resend_btn.place(relx=0.35, rely=0.72)
        #generate entry to enter otp
    frm=Frame(root)
    frm.configure(bg='sky blue')
    frm.place(relx=0,rely=.23,relwidth=1,relheight=.71)

    otp_entry = Entry(frm, font=('arial', 16, 'bold'), bd=5, bg='pink')
    verify_btn = Button(frm, command=verify, text='Verify', bg="powder blue", fg="green", font=('arial', 14, 'bold'), bd=5)

    timer_lbl = Label(frm, text="", bg='white', font=('arial', 10))
    timer_lbl.place(relx=0.72, rely=0.7)
    
    resend_btn = Button(frm, text="Resend OTP", font=('arial', 12, 'bold'), bg='orange', fg='white', bd=5, command=send_otp)
    resend_btn.place(relx=0.72, rely=0.6)

    back_btn=Button(frm,width=7,text="back",bg="grey",fg="white",font=('arial',12,'bold'),bd=5,command=back)                #back button           
    back_btn.place(relx=.0,rely=.0)

    acn_label=Label(frm,text="Account No.",bg='sky blue',font=('arial',16,'bold'))                                      #a/c no label                    
    acn_label.place(relx=.33,rely=.1)
    
    acn_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
    acn_entry.place(relx=.48,rely=.1)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",bg='sky blue',font=('arial',16,'bold'))                      #Create ACN of user
    email_lbl.place(relx=.33,rely=.22)
    
    email_entry=Entry(frm,font=('Email',16,'bold'),bd=5,bg='pink')                                                  #Entry field of user ACN
    email_entry.place(relx=.48,rely=.22)

    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='white',font=('arial',16,'bold'))                #Show and call the captcha from def function line no.9
    captcha_lbl.place(relx=.48,rely=.35)                                                              #Place The captcha field

    refresh_btn=Button(frm,text="refresh",fg="blue",font=('arial',8,'bold'),bd=5,command=refresh)           #Refresh Button to captcha
    refresh_btn.place(relx=.6,rely=.35)

    inputcap_entry=Entry(frm,font=('arial',16,'bold'),bd=5,bg='pink')                                   #Entry field of user Captcha
    inputcap_entry.place(relx=.48,rely=.46)                                                             #place the entry field of user captch              

    otp_btn=Button(frm,command=send_otp,text="send OTP",bg="powder blue",fg="green",font=('arial',14,'bold'),bd=5)            
    otp_btn.place(relx=.33,rely=.6)                                                                       
   
    reset_btn=Button(frm,text="reset",bg="powder blue",fg="blue",font=('arial',14,'bold'),bd=5)             
    reset_btn.place(relx=.62,rely=.75)

def user_screen(uacn=None):
    global frm
    for widget in root.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()

    def logout():                                                                                               #function to logout button works
        resp=messagebox.askyesno("logout","Do want to Logout?")
        if resp:
            frm.destroy()
            main_screen()
    
    def getdetail():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup

    def update_picture():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'images/{uacn}.png')

        profile_img=Image.open(f'images/{uacn}.png').resize((150,160))
        bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
        profile_img_lbl.image=bitmap_profile_img
        profile_img_lbl.configure(image=bitmap_profile_img)    

    frm=Frame(root)
    frm.configure(bg='sky blue')
    frm.place(relx=0,rely=.23,relwidth=1,relheight=.71)

    wel_label=Label(frm,text=F"Welcome, {getdetail()[1]}",bg='sky blue',font=('arial',16,'bold'),fg='dark blue')                      #welcom admin mssg show
    wel_label.place(relx=.0,rely=.0)

    logout_btn=Button(frm,width=7,text="logout",bg="grey",fg="white",font=('arial',12,'bold'),bd=5,command=logout)              #logout button to the admin
    logout_btn.place(relx=.02,rely=.84)    

    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/profile_pic.jpg"
    profile_img=Image.open(path).resize((150,160))
    bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
    profile_img_lbl=Label(frm,image=bitmap_profile_img)
    profile_img_lbl.image=bitmap_profile_img
    profile_img_lbl.place(relx=.86,rely=0)

    update_icon_img = Image.open("images/uploadd.png").resize((30, 30))  # Resize icon as needed
    update_icon_img = ImageTk.PhotoImage(update_icon_img, master=root)

    update_pic_btn = Button(frm,command=update_picture,image=update_icon_img,bg="sky blue",bd=0)           # Replace with your update function
   
    update_pic_btn.image = update_icon_img                      # Prevent garbage collection
    update_pic_btn.place(relx=.9, rely=.35)

    # update_pic_btn=Button(frm,width=11,text="Update picture",bg="dark green",fg="white",font=('arial',13,'bold'),bd=5)              #logout button to the admin
    # update_pic_btn.place(relx=.87,rely=.35)

    def check_details():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        title_lbl=Label(ifrm,text="This is check screen details",bg='white',font=('arial',16,'bold'),fg='purple')                      #place the title of manage account frame
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        Label(ifrm, text="Name:", font=('arial',14), bg='white').place(relx=0.05, rely=0.25)
        Label(ifrm, text=tup[1], font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.25)

        Label(ifrm, text="Available Balance:", font=('arial',14), bg='white').place(relx=0.05, rely=0.35)
        Label(ifrm, text=str(tup[12]), font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.35)

        Label(ifrm, text="IFSC Code:", font=('arial',14), bg='white').place(relx=0.05, rely=0.45)
        Label(ifrm, text=str(tup[10]), font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.45)

        Label(ifrm, text="Account Open Date:", font=('arial',14), bg='white').place(relx=0.05, rely=0.55)
        Label(ifrm, text=str(tup[11]), font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.55)

        Label(ifrm, text="Email:", font=('arial',14), bg='white').place(relx=0.05, rely=0.65)
        Label(ifrm, text=tup[3], font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.65)

        Label(ifrm, text="Mobile No:", font=('arial',14), bg='white').place(relx=0.05, rely=0.75)
        Label(ifrm, text=tup[4], font=('arial',14,'bold'), bg='white', fg='green').place(relx=0.35, rely=0.75)

        details_lbl=Label(ifrm,text="",bg='white',fg='red',font=('arial',16,'bold'))
        details_lbl.place(relx=.2,rely=.2)

    check_btn=Button(frm,width=11,text="Check details",bg="purple",fg="white",font=('arial',13,'bold'),bd=5,command=check_details)              #logout button to the admin
    check_btn.place(relx=.02,rely=.09)

    def deposit_screen():
        def deposit():
            try:
                # Step 1: Get amount and update balance
                uamt = float(amt_entry.get())
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'update accounts set accounts_bal = accounts_bal + ? where accounts_acno = ?'
                curobj.execute(query, (uamt, uacn))
                conobj.commit()
                conobj.close()

                # Step 2: Fetch updated balance
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'select accounts_bal from accounts where accounts_acno = ?'
                curobj.execute(query, (uacn,))
                ubal = curobj.fetchone()[0]
                conobj.close()

                balance_label = Label(ifrm, text=f"₹{uamt:.2f} has been deposited.\nUpdated Balance: ₹{ubal:.2f}",fg='green', bg='white', font=('arial', 12, 'bold'))
                balance_label.place(relx=0.26, rely=0.55)  # adjust position if needed

                # Step 3: Add transaction to statement
                t = str(time.time())
                utxnid = 'txn91' + t[:t.index('.')]
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'insert into stmts values (?, ?, ?, ?, ?, ?)'
                curobj.execute(query, (uacn, uamt, 'Cr.', time.strftime("%d-%m-%Y %r"), ubal, utxnid))
                conobj.commit()
                conobj.close()

                # Step 4: Fetch user's email
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'select accounts_email from accounts where accounts_acno = ?'
                curobj.execute(query, (uacn,))
                user_email = curobj.fetchone()[0]
                conobj.close()

                # Step 5: Send email
                msg = EmailMessage()
                msg['Subject'] = 'Deposit Confirmation'
                msg['From'] = 'shivammishraa087@gmail.com'
                msg['To'] = user_email
                msg.set_content(
                    f"Dear Customer,\n\n"
                    f"An amount of ₹{uamt:.2f} has been successfully deposited to your account ({uacn}).\n"
                    f"Current Balance: ₹{ubal:.2f}\n"
                    f"Transaction ID: {utxnid}\n"
                    f"Date: {time.strftime('%d-%m-%Y %r')}\n\n"
                    f"Thank you for banking with us.\n\n"
                    f"- MOON BANK")
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465,timeout=10) as smtp:
                        smtp.login('shivammishraa087@gmail.com', 'xxxxxxxxx')  # app passwor mentioned
                        smtp.send_message(msg)

                # Step 6: Notify user
                    messagebox.showinfo("Deposit", f"₹{uamt} Amount Deposited Successfully.\nA confirmation email has been sent.")

                except (smtplib.SMTPConnectError, socket.gaierror, OSError):
                    messagebox.showwarning("Network Issue", "Deposit successful, but failed to send confirmation email due to internet issues.")

            finally:
                frm.destroy()
                user_screen(uacn)
            
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        title_lbl=Label(ifrm,text="This is deposit screen details",bg='white',font=('arial',16,'bold'),fg='purple')                      #place the title of manage account frame
        title_lbl.pack()

        amt_lbl=Label(ifrm, text="Amount", bg='white', font=('arial', 16, 'bold'))
        amt_lbl.place(relx=.26, rely=.15)

        amt_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        amt_entry.place(relx=.44, rely=.15)
        amt_entry.focus()

        dep_btn = Button(ifrm, text="Deposit", bg="powder blue", fg="green",font=('arial', 14, 'bold'), bd=5, command=deposit)
        dep_btn.place(relx=.45, rely=.32)
        
    deposit_btn=Button(frm,width=11,text="Deposit",bg="red",fg="white",font=('arial',13,'bold'),bd=5,command=deposit_screen)              #logout button to the admin
    deposit_btn.place(relx=.02,rely=.21)

    def withdraw_screen():
        def withdraw():
            try:
            # Step 1: Get amount and update balance
                uamt = float(amt_entry.get())
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'select accounts_bal from accounts where accounts_acno = ?'
                curobj.execute(query, (uacn,))
                ubal = curobj.fetchone()[0]
                conobj.close()

                if ubal>=uamt:
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'update accounts set accounts_bal = accounts_bal-? where accounts_acno = ?'
                    curobj.execute(query, (uamt, uacn))
                    conobj.commit()
                    conobj.close()

                        # Step 2: Fetch updated balance
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'select accounts_bal from accounts where accounts_acno = ?'
                    curobj.execute(query, (uacn,))
                    ubal = curobj.fetchone()[0]
                    conobj.close()

                    balance_lbl = Label(ifrm, text=f"₹{uamt:.2f} has been deposited.\nUpdated Balance: ₹{ubal:.2f}",fg='green', bg='white', font=('arial', 12, 'bold'))
                    balance_lbl.place(relx=0.26, rely=0.55)

                        # Step 3: Add transaction to statement
                    t = str(time.time())
                    utxnid = 'txn91' + t[:t.index('.')]
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'insert into stmts values (?, ?, ?, ?, ?, ?)'
                    curobj.execute(query, (uacn, uamt, 'Dr.', time.strftime("%d-%m-%Y %r"), ubal-uamt, utxnid))
                    conobj.commit()
                    conobj.close()

                    # Step 4: Fetch user's email
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'select accounts_email from accounts where accounts_acno = ?'
                    curobj.execute(query, (uacn,))
                    user_email = curobj.fetchone()[0]
                    conobj.close()

                    msg = EmailMessage()
                    msg['Subject'] = 'Withdrawal Confirmation'
                    msg['From'] = 'shivammishraa087@gmail.com'
                    msg['To'] = user_email
                    msg.set_content(
                        f"Dear Customer,\n\n"
                        f"You have successfully withdrawn ₹{uamt:.2f} from your account ({uacn}).\n"
                        f"Current Balance: ₹{ubal:.2f}\n"
                        f"Transaction ID: {utxnid}\n"
                        f"Date: {time.strftime('%d-%m-%Y %r')}\n\n"
                        f"Thank you for banking with us.\n\n"
                        f"- MOON BANK")
                    
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context, timeout=10) as smtp:
                        smtp.login('shivammishraa087@gmail.com', 'xxxxxxxxx')  #app password metioned
                        smtp.send_message(msg)

                    messagebox.showinfo("Withdraw", f"₹{uamt} Amount Withdraw Successfully.\nA confirmation email has been sent.")
                    frm.destroy()
                    user_screen(uacn)
                else:
                    messagebox.showerror("Withdraw",f"Insufficient Bal {ubal}")     
            except (smtplib.SMTPException, socket.error):
                messagebox.showwarning("Network Issue","Withdrawal successful, but failed to send confirmation email due to internet issues.")

            except Exception as e:
                    messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            
            # net_label = Label(ifrm, text="Checking Network....", fg='red', bg='white', font=('arial', 10, 'italic'))
            # net_label.place(relx=0.3, rely=0.9)
            # ifrm.update()


        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        title_lbl=Label(ifrm,text="This is withdraw screen details",bg='white',font=('arial',16,'bold'),fg='purple')                      #place the title of manage account frame
        title_lbl.pack()

        amt_lbl=Label(ifrm, text="Amount", bg='white', font=('arial', 16, 'bold'))
        amt_lbl.place(relx=.26, rely=.15)

        amt_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        amt_entry.place(relx=.44, rely=.15)
        amt_entry.focus()

        dep_btn = Button(ifrm, text="Withdraw", bg="powder blue", fg="green",font=('arial', 14, 'bold'), bd=5, command=withdraw)
        dep_btn.place(relx=.45, rely=.32)

    withdraw_btn=Button(frm,width=11,text="Withdraw",bg="purple",fg="white",font=('arial',13,'bold'),bd=5,command=withdraw_screen)              #logout button to the admin
    withdraw_btn.place(relx=.02,rely=.33)

    def update_screen():
        def update_db():
            uname=name_entry.get()
            upass=pass_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            unomaniee=nomainee_entry.get()
            uadd=add_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='Update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=?,accounts_nom=?,accounts_address=? where accounts_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,unomaniee,uadd,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Profile Updated")
            frm.destroy()
            user_screen(uacn)

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        title_lbl=Label(ifrm,text="This is update screen details",bg='white',font=('arial',16,'bold'),fg='purple')                      #place the title of manage account frame
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        name_lbl=Label(ifrm,text="Name",bg='white',font=('arial',16,'bold'))                                     #this is admin screen details to open a a/c                 
        name_lbl.place(relx=.07,rely=.1)
        
        name_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        name_entry.place(relx=.07,rely=.19)
        name_entry.insert(0,tup[1])
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",bg='white',font=('arial',16,'bold'))                      #Create ACN of user
        email_lbl.place(relx=.07,rely=.3)
    
        email_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  #Entry field of user ACN
        email_entry.place(relx=.07,rely=.39)
        email_entry.insert(0,tup[3])

        mob_lbl=Label(ifrm,text="Mob",bg='white',font=('arial',16,'bold'))                     
        mob_lbl.place(relx=.07,rely=.5)
        
        mob_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        mob_entry.place(relx=.07,rely=.59)
        mob_entry.insert(0,tup[4])
    
        add_lbl=Label(ifrm,text="Address",bg='white',font=('arial',16,'bold'))                     
        add_lbl.place(relx=.65,rely=.1)
        
        add_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        add_entry.place(relx=.65,rely=.19)
        add_entry.insert(0,tup[6])
        

        nomainee_lbl=Label(ifrm,text="Nomaniee",bg='white',font=('arial',16,'bold'))                     
        nomainee_lbl.place(relx=.65,rely=.3)
        
        nomainee_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')                                                  
        nomainee_entry.place(relx=.65,rely=.39)
        nomainee_entry.insert(0,tup[8])

        pass_lbl=Label(ifrm,text="Pass",bg='white',font=('arial',16,'bold'))                     
        pass_lbl.place(relx=.65,rely=.5)

        pass_entry=Entry(ifrm,font=('arial',16,'bold'),bd=5,bg='pink')
        pass_entry.place(relx=.65,rely=.59)
        pass_entry.insert(0,tup[2])
       
        update_btn=Button(ifrm, text="Update", font=('arial', 14, 'bold'), bg='lightgreen', fg='black',command=update_db)
        update_btn.place(relx=.48,rely=.85)


    update_btn=Button(frm,width=11,text="Update",bg="red",fg="white",font=('arial',13,'bold'),bd=5,command=update_screen)              #logout button to the admin
    update_btn.place(relx=.02,rely=.44)

    def transfer_screen():
        def transfer():
            toacn=to_entry.get()
            uamt = float(amt_entry.get())
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select * from accounts where accounts_acno = ?'
            curobj.execute(query, (toacn,))
            to_tup= curobj.fetchone()
            conobj.close()

            if to_tup==None:
                messagebox.showerror("Transfer","To ACN does not exist")
                return

            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select accounts_bal from accounts where accounts_acno = ?'
            curobj.execute(query, (uacn,))
            ubal = curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query_deduct = 'update accounts set accounts_bal = accounts_bal-? where accounts_acno = ?'
                query_credit = 'update accounts set accounts_bal = accounts_bal+? where accounts_acno = ?'
                
                curobj.execute(query_deduct, (uamt, uacn))
                curobj.execute(query_credit, (uamt, toacn))
                conobj.commit()
                conobj.close()

                # Step 2: Fetch updated balance
                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                query = 'select accounts_bal from accounts where accounts_acno = ?'
                curobj.execute(query, (uacn,))
                ubal = curobj.fetchone()[0]
                conobj.close()

                t = str(time.time())
                utxnid1='txndr91' + t[:t.index('.')]
                utxnid2='txncr78' + t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='insert into stmts values (?, ?, ?, ?, ?, ?)'
                query2='insert into stmts values (?, ?, ?, ?, ?, ?)'

                curobj.execute(query1, (uacn, uamt, 'Dr.', time.strftime("%d-%m-%Y %r"), ubal-uamt, utxnid1))
                curobj.execute(query2, (toacn, uamt, 'Cr.', time.strftime("%d-%m-%Y %r"), ubal+uamt, utxnid2))
                conobj.commit()
                conobj.close()

                conobj = sqlite3.connect(database='bank.sqlite')
                curobj = conobj.cursor()
                curobj.execute('select accounts_email from accounts where accounts_acno = ?', (uacn,))
                user_email = curobj.fetchone()[0]
                conobj.close()

                sender_email = "shivammishraa087@gmail.com"
                sender_password = "xxxxx"   #app password mentioned
                receiver_email = user_email
                
                subject = "Amount Transfer Notification"
                body = f"""Dear user ({uacn}),\n\nYou have successfully transferred ₹{uamt} to account {toacn}.
                Your new balance is ₹{ubal}.\n\nThank you for banking with us.\n\nBest,\nMoon Bank"""
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                except Exception as e:
                    print(f"Error sending email: {e}")
                
                balance_lbl = Label(ifrm,text=f"Your remaining balance is ₹{ubal}",bg='white',font=('arial', 14, 'bold'),fg='green')
                balance_lbl.place(relx=0.26, rely=0.65)


                messagebox.showinfo("Transfer",f"{uamt} Amount Transfer")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f"Isufficient Bal {ubal}")


        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        title_lbl=Label(ifrm,text="This is transfer screen details",bg='white',font=('arial',16,'bold'),fg='purple')                      #place the title of manage account frame
        title_lbl.pack()

        to_lbl=Label(ifrm, text="To ACN", bg='white', font=('arial', 16, 'bold'))
        to_lbl.place(relx=.26, rely=.15)

        to_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        to_entry.place(relx=.44, rely=.15)
        to_entry.focus()

        amt_lbl=Label(ifrm, text="Amount", bg='white', font=('arial', 16, 'bold'))
        amt_lbl.place(relx=.26, rely=.32)

        amt_entry = Entry(ifrm, font=('arial', 16, 'bold'), bd=5, bg='pink')
        amt_entry.place(relx=.44, rely=.32)

        tr_btn = Button(ifrm, text="Transfer", bg="powder blue", fg="green",font=('arial', 14, 'bold'), bd=5, command=transfer)
        tr_btn.place(relx=.45, rely=.45)

    transfer_btn=Button(frm,width=11,text="Transfer",bg="Purple",fg="white",font=('arial',13,'bold'),bd=5,command=transfer_screen)              #logout button to the admin
    transfer_btn.place(relx=.02,rely=.56)

    def history_screen(uacn,parent):
        
        ifrm = tk.Frame(parent, highlightthickness=2, highlightbackground='black', bg='white')
        ifrm.place(relx=0.17, rely=0.1, relwidth=0.66, relheight=0.8)

        tk.Label(ifrm, text="Transaction History", bg='white',font=('Arial', 14, 'bold'), fg='purple').pack(pady=8)
        search_var = tk.StringVar()
        tk.Label(ifrm, text="Search by Txn ID:", bg='yellow').pack(pady=2)
        tk.Entry(ifrm, textvariable=search_var, bd=3, font=('Arial', 10)).pack(pady=2)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        cols = ("Txn ID", "Amount", "Txn type", "Updated Bal", "Date")
        tree = ttk.Treeview(ifrm, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor=tk.CENTER, width=120)

        vsb = ttk.Scrollbar(ifrm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill='both', expand=True, pady=8)

        def load_data(*args):
            query_id = search_var.get().strip()
            tree.delete(*tree.get_children())

            sql = """
                SELECT stmts_txnid, stmts_amt, stmts_type, stmts_update_bal, stmts_date
                FROM stmts
                WHERE stmts_acn = ?
            """
            params = [uacn]
            if query_id:
                sql += " AND stmts_txnid LIKE ?"
                params.append(f"%{query_id}%")

            try:
                conn = sqlite3.connect('bank.sqlite')
                rows = conn.execute(sql, params).fetchall()
                conn.close()
            except sqlite3.Error as e:
                tree.insert("", "end", values=(f"DB error: {e}", "", "", "", ""))
                return

            if not rows:
                tree.insert("", "end", values=("No results found", "", "", "", ""))
            else:
                for row in rows:
                    tree.insert("", "end", values=row)

        search_var.trace_add('write', load_data)  # trace sends *args :contentReference[oaicite:6]{index=6}
        load_data()

    global help_btn
    help_btn = Button(frm, width=9, text="Help Desk", bg="orange", fg="black", font=('arial',9,'bold'), bd=5,command=open_help_desk)                 #create the help desk button
    help_btn.place(relx=.92, rely=.9)

    history_btn=Button(frm,width=11,text="Transaction",bg="red",fg="white",font=('arial',13,'bold'),bd=5,command=lambda:history_screen(uacn,frm))              #logout button to the admin
    history_btn.place(relx=.02,rely=.68)


update_datetime()
scroll_header()
animate_left()
animate_right()
scroll_text()                                                                                       #call function to scrolling text in the footer
main_screen()                                                                                       #call function
root.mainloop()                                                                                     #root window visible