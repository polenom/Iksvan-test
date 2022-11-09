from smtplib import SMTPAuthenticationError

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from main.celery import app

User = get_user_model()


@app.task
def add():
    users = User.objects.all()
    for user in users:
        if not user.email:
            continue
        print(user.email)
        message = \
            f"""Hello,{user.username}
You spend {user.balance}"""
        try:
            send_mail("Statistic from site", message, "vitalimit88@gmail.com", [user.email])
        except (SMTPAuthenticationError, OSError):
            continue
