# Generated by Django 3.2.7 on 2021-10-07 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_img_badge_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badge',
            old_name='image_url',
            new_name='img',
        ),
        migrations.CreateModel(
            name='EventComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.friend')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.event')),
            ],
        ),
    ]
