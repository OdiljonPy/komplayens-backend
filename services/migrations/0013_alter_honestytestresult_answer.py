# Generated by Django 5.1.4 on 2025-01-21 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_alter_corruptionrisk_short_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='honestytestresult',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.honestytestanswer', verbose_name='Ответ'),
        ),
    ]
