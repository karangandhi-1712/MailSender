import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def load_env_file(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, mode='r', encoding='utf-8') as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()

# Set SMTP configuration from environment
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
# If using Gmail, use an App Password, not your standard account password
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')

if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError('SENDER_EMAIL and SENDER_PASSWORD must be set in .env or environment.')

DRAFTS_CSV = 'drafts.csv'

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Connect to the server and send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls() # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# Read the reviewed drafts and send
with open(DRAFTS_CSV, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        company = row["Company"]
        email = row["Email"]
        subject = row["Subject"]
        body = row["Body"]
        
        print(f"Sending email to {company} at {email}...")
        try:
            send_email(email, subject, body)
            print("Success.")
        except Exception as e:
            print(f"Failed to send to {email}. Error: {e}")