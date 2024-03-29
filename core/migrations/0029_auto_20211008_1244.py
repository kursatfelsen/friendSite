# Generated by Django 3.2.7 on 2021-10-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20211008_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
        migrations.AlterField(
            model_name='eventcomment',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
        migrations.AlterField(
            model_name='friend',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
        migrations.AlterField(
            model_name='friendgroup',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
        migrations.AlterField(
            model_name='location',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
        migrations.AlterField(
            model_name='vote',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default="2021-01-05 06:00:00.000000-09:00"),
        ),
    ]
