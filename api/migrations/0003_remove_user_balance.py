# Generated by Django 4.1.3 on 2022-11-08 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_category_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='balance',
        ),
    ]