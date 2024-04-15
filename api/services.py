from random import choice
from string import ascii_lowercase, digits
from google.cloud.firestore_v1 import FieldFilter
import smtplib
from email.message import EmailMessage
from api.firebase_config import usersCollection
from ingridge.settings import EMAIL_PASSWORD, EMAIL


def get_user_by_email(email: str):
    user_doc = usersCollection.where(filter=FieldFilter('email', '==', email)).limit(1).get()
    if len(user_doc) > 0:
        return user_doc[0].to_dict()
    return None


def generate_otp(length: int) -> str:
    characters = ascii_lowercase + digits
    otp = []
    for i in range(length):
        otp.append(choice(characters))
    return ''.join(otp)


def send_email(subject='', body='', email=''):

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # server.set_debuglevel(1)
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(create_email(subject, body, email))

        return True
    except Exception as e:
        print(e)
        return str(e)


def create_email(subject='', body='', email=''):

    message = EmailMessage()
    message["From"] = EMAIL
    message["To"] = email
    message["Subject"] = subject
    html_body = "<html><body><p>{body}</p></body></html>"
    message.set_content(html_body.format(body=body), subtype='html')
    print(True)
    return message
