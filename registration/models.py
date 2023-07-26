from django.contrib.auth.models import User
from django.db import models

from event.models import Answer, EventRecord
from organizer.models import organizerRecord
from .utils import registration_unique_slug, transaction_unique_slug


# Create your models here.
class TransactionRecord(models.Model):
    transaction_id = models.SlugField(unique=True)
    amount = models.FloatField()
    remark = models.CharField(max_length=55, default="-")
    registration_id = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = transaction_unique_slug(self, self.registration_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id


class RegistrationRecord(models.Model):
    registration_id = models.SlugField(unique=True)
    transaction_id = models.ManyToManyField(TransactionRecord)
    amount = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    cancel = models.BooleanField(default=False)
    organizer = models.ForeignKey(organizerRecord, on_delete=models.PROTECT)
    client = models.ForeignKey(Answer, on_delete=models.PROTECT) #dynamic forminte table ann ivide vendath
    event = models.ForeignKey(EventRecord, on_delete=models.PROTECT, default='')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = registration_unique_slug(self, self.event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_id

class Question(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    MULTIPLE_CHOICE = 'multiple_choice'
    TEXTAREA = 'textarea'
    IMAGE = 'image'

    QUESTION_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TEXTAREA, 'Text Area'),
        (IMAGE, 'Image'),
    ]

    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)

class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
