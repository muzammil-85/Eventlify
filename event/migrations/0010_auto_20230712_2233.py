# Generated by Django 2.2.24 on 2023-07-12 17:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20230709_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrecord',
            name='venue',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]