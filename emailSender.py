import config

import smtplib
from datetime import datetime

class Email:
    def __enter__(self):
        return self
    def __init__(self, address, password):
        self.address = address
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(address, password)
    def send_email(self, destAddress, subject, msg):
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        print("Sending email...")
        self.server.sendmail(self.address, destAddress, message)
    def __exit__(self, type, value, traceback):
        self.server.quit()

def send_email(msg):
    subject = "Message from Spot: " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    try:
        with Email(config.SENDER_EMAIL_ADDRESS, config.SENDER_EMAIL_PASSWORD) as email:
            email.send_email(config.RECEIVER_EMAIL_ADDRESS, subject, msg)
    except Exception as ex:
        print("Email failed to send.")
        print(ex)

if __name__ == "__main__":
    send_email("This is an example email.")
