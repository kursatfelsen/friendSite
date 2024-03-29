# Generated by Django 3.2.7 on 2021-10-06 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_badge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='owner',
        ),
        migrations.CreateModel(
            name='BadgeFriendRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_relation', to='core.badge')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badge_relation', to='core.friend')),
            ],
        ),
    ]
