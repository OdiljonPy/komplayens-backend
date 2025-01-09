# Generated by Django 5.1.4 on 2025-01-09 18:35

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('short_desc', models.TextField(max_length=300, verbose_name='Краткое описание')),
                ('link', models.CharField(max_length=40, verbose_name='Ссылка')),
                ('type', models.IntegerField(choices=[(1, 'About System'), (2, 'About Violation Report'), (3, 'About Conflict of Interest'), (4, 'About Corruption Risk')], default=1, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'О нас',
                'verbose_name_plural': 'О нас',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=250, verbose_name='Вопрос')),
                ('answer', tinymce.models.HTMLField(verbose_name='Отвечать')),
                ('type', models.IntegerField(choices=[(1, 'FAQ System'), (2, 'FAQ Organization'), (3, 'FAQ Conflict of interest')], default=1, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Часто задаваемый вопрос',
                'verbose_name_plural': 'Часто задаваемые вопросы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Округ',
                'verbose_name_plural': 'Округи',
                'ordering': ('-created_at',),
            },
        ),
    ]
