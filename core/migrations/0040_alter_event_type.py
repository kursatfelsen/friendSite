# Generated by Django 3.2.7 on 2021-10-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('0', 'None'), ('1', 'Breakfast'), ('2', 'Lunch'), ('3', 'Dinner'), ('5', 'Entertainment'), ('8', 'Work'), ('4', 'Meeting'), ('6', 'Outdoor'), ('7', 'Vacation'), ('9', 'Study')], default='0', max_length=1),
        ),
    ]