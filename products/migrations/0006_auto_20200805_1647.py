# Generated by Django 3.0.7 on 2020-08-05 14:47

from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200805_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='component',
        ),
        migrations.AddField(
            model_name='product',
            name='file',
            field=private_storage.fields.PrivateFileField(default=0, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='', verbose_name='File'),
            preserve_default=False,
        ),
    ]