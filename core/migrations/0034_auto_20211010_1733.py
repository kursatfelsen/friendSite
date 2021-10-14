# Generated by Django 3.2.7 on 2021-10-10 17:33

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20211010_1608'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='vote',
            managers=[
                ('yeah_votes', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='badge',
            name='description',
            field=models.TextField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='badge',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friendgroup',
            name='is_private',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Latitude'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Longitude'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Phone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='photo_url',
            field=models.CharField(blank=True, default='', max_length=2000, verbose_name='Photo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='rating',
            field=models.CharField(blank=True, default='', max_length=40, verbose_name='Rating'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='type',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='website',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Website'),
            preserve_default=False,
        ),
    ]
