import sqlite3
import smtplib
import time
from email.message import EmailMessage

conobj=sqlite3.connect(database='bank.sqlite')
curobj=conobj.cursor()
query = 'SELECT accounts_email FROM accounts WHERE accounts_acno = ?'
curobj.execute(query, (uacn,))
user_email = curobj.fetchone()[0]
conobj.close()

msg = EmailMessage()
msg['Subject'] = 'Deposit Confirmation'
msg['From'] = 'shivammishraa087@gmail.com'  # Your sender email
msg['To'] = user_email
msg.set_content(
        f"Dear Customer,\n\n"
        f"An amount of ₹{uamt:.2f} has been successfully deposited to your account ({uacn}).\n"
        f"Current Balance: ₹{ubal:.2f}\n"
        f"Transaction ID: {utxnid}\n"
        f"Date: {time.strftime('%d-%m-%Y %r')}\n\n"
        f"Thank you for banking with us.\n\n"
        f"- Your Bank"
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('shivammishraa087@gmail.com', 'mzjz fuis mtak ovqz')  # Use your app password
            smtp.send_message(msg)