# Generated by Django 3.2.7 on 2021-09-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='friend',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='friend',
            name='second_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
