import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ORG_MAIL_ADRESS = 'romanfcb123@gmail.com'
ORG_MAIL_PASSWORD = 'gtqu pjgy xdxu nmyj'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(to_address, subject, message):
    """Отправляет email."""
    from_address = ORG_MAIL_ADRESS
    password = ORG_MAIL_PASSWORD
    
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()