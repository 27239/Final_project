import smtplib
from email.mime.text import MIMEText

# ===== CHANGE THESE =====
SENDER_EMAIL = "mokariyay5@gmail.com"
APP_PASSWORD = "ijnt zdmb dqlw vkrl"
RECEIVER_EMAIL = "mokariyay5@gmail.com"
# ========================

def send_alert(server_name, message):

    subject = f"Alert: {server_name}"

    body = f"""
Infrastructure Monitoring Alert

Server : {server_name}

Message :

{message}
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("Email Sent Successfully")
