# Generated by Django 2.2.24 on 2023-07-21 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20230720_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='EventRecord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='event.EventRecord'),
        ),
    ]