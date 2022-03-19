from django.db import models

# Create your models here.

class User(models.Model):
    username= models.CharField(max_length=100)
    email= models.EmailField()
    password= models.CharField(max_length=100)
    profile_pic= models.CharField(max_length=200)
    type= models.CharField(max_length=200,default='user')

    def __str__(self):
        return self.username
