# Generated by Django 3.2.7 on 2021-09-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20210916_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='second_name',
        ),
        migrations.AddField(
            model_name='friend',
            name='img',
            field=models.TextField(blank=True),
        ),
    ]