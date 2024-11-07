import smtplib
import os
from email.message import EmailMessage
from email.utils import formataddr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values

config = dotenv_values(".env")

# Email details
# def mail(body):
#     sender_email = "mohamed.shata452002@gmail.com"

#     receiver_email = "mohamed.shata2002@gmail.com"
#     server = smtplib.SMTP("smtp.gmail.com",587)
#     server.starttls()
#     server.login(sender_email,"csag cuko puno cdga")
#     server.sendmail(sender_email,receiver_email,body)
def mail(name,body):
    sender_name = name
    sender_email = config["sender"]
    receiver_email = config["receiver_email"]
    
    # Create a MIMEText object to represent the email
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = "Your Subject Here"

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server and send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, "csag cuko puno cdga")
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
