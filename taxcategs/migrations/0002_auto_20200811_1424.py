# Generated by Django 3.0.7 on 2020-08-11 12:24

from django.db import migrations, models
import taxcategs.models


class Migration(migrations.Migration):

    dependencies = [
        ('taxcategs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryterm',
            name='image',
            field=models.ImageField(upload_to=taxcategs.models.upload_image_path),
        ),
    ]
