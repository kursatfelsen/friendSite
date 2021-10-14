# Generated by Django 3.2.7 on 2021-10-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20211013_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('1', 'Breakfast'), ('2', 'Lunch'), ('3', 'Dinner'), ('5', 'Entertainment'), ('8', 'Work'), ('4', 'Meeting'), ('6', 'Outdoor'), ('7', 'Vacation'), ('9', 'Study')], max_length=1),
        ),
    ]
