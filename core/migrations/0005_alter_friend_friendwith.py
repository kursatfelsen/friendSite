# Generated by Django 3.2.7 on 2021-09-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_friend_friendwith'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friendWith',
            field=models.ManyToManyField(related_name='_core_friend_friendWith_+', to='core.Friend'),
        ),
    ]
