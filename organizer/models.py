from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class organizerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=30,null=True,blank=True)
    Lname = models.CharField(max_length=30,null=True,blank=True)
    Mobile = models.CharField(null=True,blank=True,max_length=30)
    Email = models.EmailField(null=True,blank=True)
    Dob = models.DateField(null=True,blank=True)
    Address = RichTextUploadingField(default='')
    Id_type = models.CharField(max_length=15,null=True,blank=True)
    status = models.CharField(max_length=30,default='unverified')
    Id_file = models.FileField(default='')
    

    def __str__(self):
        return str(self.Fname)
