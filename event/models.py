from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.utils.text import slugify

class EventRecord(models.Model):
    slug = models.SlugField(unique=True,null=True,blank=True)
    types = models.CharField(max_length=110, blank=True,default='')
    event_title = models.CharField(max_length=110, null=True, blank=True)
    event_subtitle = models.CharField(max_length=110, null=True, blank=True)
    fees = models.FloatField(default=0)
    description = RichTextUploadingField(null=True, blank=True)
    event_start_date = models.DateField(null=True, blank=True)
    event_end_date = models.DateField(null=True, blank=True)
    event_start_time = models.TimeField(null=True, blank=True)
    event_end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=50, null=True, blank=True)
    mode = models.CharField(max_length=50, null=True, blank=True)
    platform = models.CharField(max_length=50, null=True, blank=True)
    registration_start = models.DateField(null=True, blank=True)
    registration_end = models.DateField(null=True, blank=True)
    no_of_tickets = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    subcategory = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    youtube = models.CharField(max_length=50, null=True, blank=True)
    banner = models.FileField(default='')
    poster = models.FileField(default="")
    logo = models.FileField(default="")
    sponsor_logo = models.FileField(default="")
    event_booked = models.IntegerField(default=0)
    registration_open = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.registration_start and self.registration_end:
            now = timezone.now().date()
            if now >= self.registration_start and now <= self.registration_end:
                self.registration_open = True
            else:
                self.registration_open = False

        if not self.slug:
            self.slug = self.get_unique_slug(self.event_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_title

    def get_unique_slug(self, title):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        slug = slugify(f"{title}-{timestamp}")
        unique_slug = slug
        num = 1
        while EventRecord.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug


class DataList(models.Model):
    place = models.CharField(max_length=50)
    number = models.IntegerField()

    def __str__(self):
        return self.place

