# Generated by Django 5.0.6 on 2024-06-30 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flashcard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='learnerflashcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='learner',
            field=models.ManyToManyField(related_name='learner_flashcard', through='flashcard.LearnerFlashCard', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи изучающие карточки'),
        ),
        migrations.AlterUniqueTogether(
            name='learnerflashcard',
            unique_together={('user', 'flashcard')},
        ),
    ]
