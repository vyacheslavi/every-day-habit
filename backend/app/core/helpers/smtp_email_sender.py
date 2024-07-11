import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.core.config import settings


class EmailSender:
    def __init__(self):
        self.user = settings.email.login
        self.password = settings.email.password
        self.server = smtplib.SMTP(
            "smtp.gmail.com",
            587,
        )

    def send_email(self, receiver_email: str, subject: str, message: str | bytes):

        msg = MIMEMultipart()
        msg["From"] = self.user
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls(context=context)
            smtp.login(self.user, self.password)
            smtp.send_message(msg)

    def send_request_on_verify(self, receiver_email: str, token: str):
        url = f"{settings.run.url}/verificator?token={token}"
        message = f"Verification requested for user {receiver_email}. Follow the link below: {url}"
        self.send_email(receiver_email, "Verification", message)

    def send_reset_password_email(
        self,
        receiver_email: str,
        token: str,
    ):
        url = f"{settings.run.url}/v1/auth/reset-password?token={token}"
        message = f"User {receiver_email} has forgot their password. Follow the link to reset password: {url}"
        self.send_email(receiver_email, "Forgot password", message)


email_sender = EmailSender()
