import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv 

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com" 

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / "test.txt"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

def send_email(subject, receiver_email, name, appointment_date, reminder_date):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Company Name", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        I just wanted to remind you on your appointment on {appointment_date}.
        If you want to re-schedule, please email at ____@outlook.com.
        Best regards
        Dream Team.
        """
    )

    msg.add_alternative(
        f"""\
    <html>
    <body>
        <p>Hi {name},</p>
        <p>I hope you are well.</p>
        <p>I just wanted to remind you on your appointment on <strong>{appointment_date}</strong>.</p>
        <p>If you want to re-schedule, please email at <strong>____@outlook.com.</strong></p>
        <p>Best regards</p>
        <p>Dream Team.</p>
    </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    send_email(
        subject="Appointment Reminder",
        name="John Doe",
        receiver_email="theEmail@outlook.com",
        due_date="11, Aug 2022",
        invoice_no="INV-21-12-009",
        amount="5",
    )
