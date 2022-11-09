# import os
#
# from celery import Celery
# from celery.schedules import crontab
# from django.core.mail import send_mail
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
#
# app = Celery("main")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()
#
#
# # @app.on_after_configure.connect
# # def setup_periodic_tasks(sender, **kwargs):
# #     # Calls test('hello') every 10 seconds.
# #     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
# #
# #     # Calls test('world') every 30 seconds
# #     sender.add_periodic_task(30.0, test.s('world'), expires=10)
# #
# #     # Executes every Monday morning at 7:30 a.m.
# #     sender.add_periodic_task(
# #         crontab(hour=7, minute=30, day_of_week=1),
# #         test.s('Happy Mondays!'),
# #     )
#
# @app.task
# def test(x):
#     print(x)
#
# @app.task
# def send():
#     print('123')
#     send_mail("123", "123", "vitalimit88@gmail.com", ["vitalimitsevich@yandex.by"], )
#
#
# app.conf.beat_schedule = {
#     'add_every_30_sec': {
#         "task": "main.celery.test",
#         "schedule": crontab(minute="*/120"),
#         "args": ("HEloo")
#     },
#     'add_every_20_sec': {
#         "task": "test",
#         "schedule": crontab(minute="*/120"),
#         "args": ("HEloo")
#     }
# }
import datetime
import os
import time

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery()
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["api.service"])

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'api.service.add',
        'schedule': crontab(hour=7, minute=0, day_of_week="1-5"),
    },
}
