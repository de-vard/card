# Generated by Django 5.0.6 on 2024-06-30 16:40

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='FlashCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('english_word', models.CharField(max_length=100, verbose_name='Английское слово')),
                ('russian_word', models.CharField(max_length=100, verbose_name='Русское слово')),
                ('transcription', models.CharField(max_length=100, verbose_name='Транскрипция')),
                ('sound', models.FileField(blank=True, upload_to='audi/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3'])], verbose_name='Аудиофайл')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashcards', to='lesson.lesson', verbose_name='Урок')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flashcard.image', verbose_name='Фото')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='LearnerFlashCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learned_word', models.BooleanField(default=False, verbose_name='Изучено ли слово')),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcard.flashcard', verbose_name='Карточка')),
            ],
            options={
                'verbose_name': 'Статус изучения карточки',
                'verbose_name_plural': 'Статусы изучения карточек',
            },
        ),
    ]
