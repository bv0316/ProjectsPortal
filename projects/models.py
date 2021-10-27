from typing import cast
from django.contrib.admin.options import BaseModelAdmin
from django.db import models
import uuid
from users.models import Profile
from django.db.models.deletion import CASCADE
# Create your models here.
class Project(models.Model):
 owner =models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL )

 title = models.CharField(max_length=200)
 description = models.TextField(null=True, blank=True)
 source_link = models.CharField(max_length=2000, null=True, blank=True)
 featured_image = models.ImageField(null=True, blank =True, default = 'default.jpg')
 created = models.DateField(auto_now_add=True)
 id=models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
 def __str__(self):
  return self.title

class Review(models.Model):
 owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) 
 project = models.ForeignKey(Project, on_delete=CASCADE)
 body = models.TextField(null=True, blank=True)
 created = models.DateTimeField(auto_now_add=True)
 id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

 def __str__(self):
  return self.body
 class Meta:
   ordering =['-created']
