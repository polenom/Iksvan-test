import os
from smtplib import SMTPAuthenticationError

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from main.celery import app
from dotenv import load_dotenv


User = get_user_model()
load_dotenv()

@app.task
def add():
    users = User.objects.all()
    for user in users:
        if not user.email:
            continue
        message = \
            f"""Hello,{user.username}
You spend {user.balance}"""
        try:
            send_mail("Statistic from site", message, os.environ("EMAIL_ADDRESS"), [user.email])
        except (SMTPAuthenticationError, OSError):
            continue
