# Generated by Django 3.2.7 on 2021-10-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20211006_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
