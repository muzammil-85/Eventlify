# Generated by Django 2.2.24 on 2023-08-15 18:57

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('types', models.CharField(blank=True, default='', max_length=110)),
                ('event_title', models.CharField(blank=True, max_length=110, null=True)),
                ('event_subtitle', models.CharField(blank=True, max_length=110, null=True)),
                ('fees', models.FloatField(default=0)),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('event_start_date', models.DateField(blank=True, null=True)),
                ('event_end_date', models.DateField(blank=True, null=True)),
                ('event_start_time', models.TimeField(blank=True, null=True)),
                ('event_end_time', models.TimeField(blank=True, null=True)),
                ('venue', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('visibility', models.CharField(blank=True, max_length=50, null=True)),
                ('platform', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_start', models.DateField(blank=True, null=True)),
                ('registration_end', models.DateField(blank=True, null=True)),
                ('no_of_tickets', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('subcategory', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook', models.CharField(blank=True, max_length=50, null=True)),
                ('instagram', models.CharField(blank=True, max_length=50, null=True)),
                ('youtube', models.CharField(blank=True, max_length=50, null=True)),
                ('poster', models.FileField(default='', upload_to='')),
                ('event_booked', models.IntegerField(default=0)),
                ('registration_open', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200, null=True)),
                ('type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('email', 'Email'), ('textarea', 'Textarea')], max_length=20, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.EventRecord')),
                ('organizer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('response', models.CharField(max_length=200, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='event.EventRecord')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='event.Client')),
            ],
        ),
    ]
