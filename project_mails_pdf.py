import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

email='xxxxxxx@gmail.com'       #mention your gmail id
app_pass='xxxxxx'                        #mention app pass of same gmail account

def build_account_pdf(uacno, uname, udob, upass, uifsc, udate, umob, ubal, uaddress):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # 1. Border
    margin = 30
    c.setLineWidth(2)
    c.rect(margin, margin, w - 2*margin, h - 2*margin)

    # 2. Watermark
    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.translate(w/2, h/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "Moon BANK")
    c.restoreState()

    # 3. Table of details
    data = [
        ['Account No', uacno],
        ['Name', uname],
        ['DOB', udob],
        ['Password', upass],
        ['IFSC', uifsc],
        ['Opened On', udate],
        ['Balance', ubal],
        ['Mobile', umob],
        ['Address', uaddress],
    ]
    table = Table(data, colWidths=[100, 300])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.red),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]))
    table.wrapOn(c, w, h)
    table.drawOn(c, margin + 20, h - margin - table._height)

    # 4. Footer
    c.setFont("Helvetica", 9)
    c.drawCentredString(w/2, margin - 10, "© 2025 KBC Bank. All rights reserved.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def send_mail_for_openac_pdf(to_email, uacno, uname, udob, upass, uifsc, udate, umob, ubal, uaddress):
    pdf_buf = build_account_pdf(uacno, uname, udob, upass, uifsc, udate, umob, ubal, uaddress)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = 'Your Moon Bank Account Details'

    msg.attach(MIMEText(f"Dear {uname},\n\nYour account has been opened with Moon Bank.\n \nRegards, \nMoon Bank", 'plain'))

    att = MIMEApplication(pdf_buf.read(), _subtype='pdf')
    att.add_header('Content-Disposition', 'attachment', filename=f'Account_{uacno}.pdf')
    msg.attach(att)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as srv:
        srv.login(msg['From'], app_pass)
        srv.sendmail(msg['From'], to_email, msg.as_string())
