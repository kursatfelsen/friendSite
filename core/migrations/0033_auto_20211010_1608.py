# Generated by Django 3.2.7 on 2021-10-10 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20211009_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcommentlike',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='core.eventcomment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventcommentlike',
            name='liker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_comment_likes', to='core.friend'),
        ),
    ]