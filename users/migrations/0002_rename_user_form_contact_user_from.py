# Generated by Django 4.1.7 on 2023-07-26 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='user_form',
            new_name='user_from',
        ),
    ]
