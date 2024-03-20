# from config.config import settings
# from fastapi.exceptions import HTTPException
# from smtplib import SMTP_SSL
# from email.mime.text import MIMEText
#
#
# #
# # OWN_EMAIL = "giri1208srinivas@gmail.com"
# # OWN_EMAIL_PASSWORD = "afta mnuy zxpo vzdk"
#
#
# class Email:
#     def __init__(self, subject, to):
#         self.sender = settings.EMAIL_FROM
#         self.subject = subject
#         self.to = to
#         self.email_pwd = settings.EMAIL_PASSWORD
#
#         pass
#
#     async def send_email(self):
#         try:
#             msg = MIMEText("test", "html")
#             msg['Subject'] = self.subject
#             msg['From'] = self.sender
#             msg['To'] = self.to
#
#             port = 465  # For SSL
#
#             # Connect to the email server
#             server = SMTP_SSL("smtp.gmail.com", port)
#             server.login(self.sender, self.email_pwd)
#
#             # Send the email
#             server.send_message(msg)
#             server.quit()
#             return {"message": "Email sent successfully"}
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=e)

from config.config import settings
from fastapi.exceptions import HTTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from jinja2 import Environment, FileSystemLoader
import os


class Email:
    def __init__(self, subject, to, action):
        self.sender = settings.EMAIL_FROM
        self.email_pwd = settings.EMAIL_PASSWORD
        self.to = to
        self.subject = subject
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')  # Path to the templates folder
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = action

    async def send_email(self):
        try:
            # Load email template
            template = self.env.get_template(self.template + '.html')
            email_subject = "Growday Sign Up Verification(code: "+self.subject+")"
            # Render the template with context data
            html_content = template.render(subject=email_subject, message= self.subject)

            # Create email message
            msg = MIMEMultipart()
            msg['Subject'] = email_subject
            msg['From'] = self.sender
            msg['To'] = self.to

            # Attach HTML content to email
            msg.attach(MIMEText(html_content, 'html'))

            port = 465  # For SSL

            # Connect to the email server
            server = SMTP_SSL("smtp.gmail.com", port)
            server.login(self.sender, self.email_pwd)

            # Send the email
            server.sendmail(self.sender, self.to, msg.as_string())
            server.quit()
            return {"message": "Email sent successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
