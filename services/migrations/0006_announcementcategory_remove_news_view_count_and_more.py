# Generated by Django 5.1.4 on 2025-01-16 12:40

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_corruptionrisk_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория объявления',
                'verbose_name_plural': 'Категории объявлений',
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
        migrations.RemoveField(
            model_name='training',
            name='view_count',
        ),
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Просмотры'),
        ),
        migrations.AddField(
            model_name='training',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Просмотры'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', tinymce.models.HTMLField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='post/', verbose_name='Изображение')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('published_date', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.announcementcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ('-created_at',),
            },
        ),
    ]
