# Generated by Django 3.2.7 on 2021-09-16 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_event_location_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]