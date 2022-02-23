# Generated by Django 3.2.7 on 2021-10-08 12:49

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20211008_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
        migrations.AlterField(
            model_name='eventcomment',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
        migrations.AlterField(
            model_name='friend',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
        migrations.AlterField(
            model_name='friendgroup',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
        migrations.AlterField(
            model_name='location',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
        migrations.AlterField(
            model_name='vote',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True, default=timezone.now()),
        ),
    ]