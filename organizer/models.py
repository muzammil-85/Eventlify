from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

 
# Create your models here.
class organizerRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=30,null=True,blank=True)
    Lname = models.CharField(max_length=30,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Email = models.EmailField(null=True,blank=True)
    Dob = models.DateField(null=True,blank=True)
    Profile_pic = models.FileField(default='')
    Address = RichTextUploadingField(default='')
    Id_type = models.CharField(max_length=10,null=True,blank=True)
    Status = models.CharField(max_length=10,null=True,blank=True)
    Id_file = models.FileField(default='')
    

    def __str__(self):
        return str(self.user)
