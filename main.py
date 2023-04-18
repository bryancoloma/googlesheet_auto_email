from datetime import date 
import pandas as pd 
from deta import app
from send_email import send_email 

SHEET_ID = "GoogleSheet ID"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if (present >= row["reminder_date"].date()) and (row["confirmed"] == "no"):
            send_email(
                subject=f'Upcoming Muscleology Appointment',
                receiver_email=row["email"],
                name=row["name"],
                reminder_date=row["reminder_date"].strftime("%b %d, %Y"), 
                appointment_date=row["appointment_date"].strftime("%b %d, %Y")  
            )
            email_counter += 1
    return f"Total Emails Sent: {email_counter}"

df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)

@app.lib.cron()
def cron_job(event):
    df = load_df(URL)
    result = query_data_and_send_emails(df)
    return result