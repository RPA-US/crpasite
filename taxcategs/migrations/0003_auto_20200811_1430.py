# Generated by Django 3.0.7 on 2020-08-11 12:30

from django.db import migrations, models
import taxcategs.models


class Migration(migrations.Migration):

    dependencies = [
        ('taxcategs', '0002_auto_20200811_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryterm',
            name='image',
            field=models.ImageField(blank=True, upload_to=taxcategs.models.upload_image_path),
        ),
    ]