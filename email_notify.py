import smtplib
# This requires a directory, info/ , and two files within:
#  a blank __init__.py file and a mail_info file which contains
#  the mi.* variables below.
import info.mail_info as mi

#Email Variables
SMTP_SERVER    = 'smtp.gmail.com'      #Email Server (don't change!)
SMTP_PORT      = 587                   #Server Port (don't change!)
GMAIL_USERNAME = mi.sender_gmail_username
GMAIL_PASSWORD = mi.sender_gmail_password
RCPNT_USERNAME = mi.recpnt_email_username

def sendmail(content):
     
    #Create Headers
    headers = ["From: " + GMAIL_USERNAME, "Subject: THERMOSTAT TERMINATED", "To: " + RCPNT_USERNAME,
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    #Connect to Gmail Server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    #Login to Gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Send Email & Exit
    session.sendmail(GMAIL_USERNAME, RCPNT_USERNAME, headers + "\r\n\r\n" + content)
    session.quit
    
    
if __name__ == "__main__":
    sendmail( "This is a test." )