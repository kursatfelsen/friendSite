# Generated by Django 3.2.7 on 2021-09-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210921_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attender',
            field=models.ManyToManyField(blank=True, null=True, related_name='attending_set', to='core.Friend'),
        ),
    ]