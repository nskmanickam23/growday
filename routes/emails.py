from config.config import settings
from fastapi.exceptions import HTTPException
from smtplib import SMTP_SSL
from email.mime.text import MIMEText


#
# OWN_EMAIL = "giri1208srinivas@gmail.com"
# OWN_EMAIL_PASSWORD = "afta mnuy zxpo vzdk"


class Email:
    def __init__(self, subject, to):
        self.sender = settings.EMAIL_FROM
        self.subject = subject
        self.to = to
        self. email_pwd = settings.EMAIL_PASSWORD

        pass

    async def send_email(self):
        try:
            msg = MIMEText("test", "html")
            msg['Subject'] = self.subject
            msg['From'] = self.sender
            msg['To'] = self.to

            port = 465  # For SSL

            # Connect to the email server
            server = SMTP_SSL("smtp.gmail.com", port)
            server.login(self.sender, self.email_pwd)

            # Send the email
            server.send_message(msg)
            server.quit()
            return {"message": "Email sent successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=e)
