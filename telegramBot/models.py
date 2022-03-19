from django.db import models

# Create your models here.
class Telegram_Accounts(models.Model):
    userid= models.CharField(max_length=100)
    hash_id= models.TextField()
    hash_key= models.TextField()
    number= models.CharField(max_length=120)
    session_file= models.TextField()
    sleep_time= models.CharField(max_length=120,default=2)
    sleep_time_first= models.CharField(max_length=120,default=2)
    def __str__(self):
        return self.number

class Telegram_Groups(models.Model):
    userid= models.CharField(max_length=100)
    account_id= models.CharField(max_length=100)
    group_name= models.TextField()
    def __str__(self):
        return self.group_name

class Telegram_Questions(models.Model):
    userid= models.CharField(max_length=100)
    account_id= models.CharField(max_length=100)
    questions= models.TextField()
    def __str__(self):
        return self.questions

class Telegram_Answers(models.Model):
    userid= models.CharField(max_length=100)
    account_id= models.CharField(max_length=100)
    answers= models.TextField()
    def __str__(self):
        return self.answers

class Schedule_Messages(models.Model):
    userid= models.CharField(max_length=100)
    message = models.TextField()
    account_id= models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    delay = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default="text")
    def __str__(self):
        return self.message