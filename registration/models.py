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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    organizer = models.ForeignKey(organizerRecord, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    event = models.ForeignKey(EventRecord, on_delete=models.CASCADE, default='')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = registration_unique_slug(self, self.event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_id

class PaymentRecord(models.Model):

    amount = models.CharField(max_length=100,null=True)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    event = models.ForeignKey(EventRecord, on_delete=models.CASCADE, default='')
    organizer = models.ForeignKey(organizerRecord, on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.transaction_id:
    #         self.transaction_id = transaction_unique_slug(self, self.registration_id)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id