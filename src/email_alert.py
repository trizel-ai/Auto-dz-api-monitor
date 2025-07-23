import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body):
    sender_email = "admintrizel@icloud.com"
    receiver_email = "admintrizel@icloud.com"
    password = "fygq-gxbz-hxiw-zbsx"  # كلمة مرور التطبيق من Apple ID

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.mail.me.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("✅ Email alert sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
