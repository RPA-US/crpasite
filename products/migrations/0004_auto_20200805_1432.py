# Generated by Django 3.0.7 on 2020-08-05 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200805_1356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='file',
            new_name='component',
        ),
    ]
