import gmail



def send_mail_for_openac(to_mail,uacno,uname,upass,udate,uifsc,ubal,uaddress,umob,udob):
    try:
        con=gmail.GMail('shivammishraa087@gmail.com','mzjz fuis mtak ovqz')
        sub='Account opened with KBC Bank'
        
        body=f"""Dear{uname},
        Your account has beem opened successfully with KBC Bank and details are
        
    Name : {uname}
    DOB : {udob}
    ACN : {uacno}
    IFSC : {uifsc}
    Pass : {upass}
    Open date : {udate}
    Mob : {umob}
    Bal : {ubal}
    Address : {uaddress}

    Kindly change your password  whenyou login first time
    Thanks
    ABC Bank
    Noida"""

        msg=gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)
        return "mail sent successfully"
    except:
        return "Something went wrong"

def send_otp(to_mail, uname, uacno, uotp):
    con=gmail.GMail('shivammishraa087@gmail.com','mzjz fuis mtak ovqz')
    sub='OTP for password recovery'
    body=f"""Dear {uname},
        Your OTP to get password : {uotp}
        
    ACN : {uacno}

    Kindly verify the otp to application
    Thanks
    ABC Bank
    Noida"""

    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)




# net_label = Label(frm, text="Please wait... Your network may be slow.", fg='red', bg='white', font=('arial', 10, 'italic'))
# net_label.place(relx=0.3, rely=0.9)