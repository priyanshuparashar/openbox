from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here. sure!
# class Message(models.Model):
#     room
class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Contact(models.Model):
    sender=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    c_email=models.EmailField(null=False)
    c_message=models.TextField(null=True)
    c_send_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.c_message)
    

class Rooms(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    # participants=
    updated=models.DateTimeField(auto_now=True) # time stamp crepated everytime it is saved 
    created=models.DateTimeField(auto_now_add=True) ##time stamp created at the first time
    
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.name)

    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Rooms', on_delete=models.SET_NULL, null=True)
    body = models.TextField(null=True)
    updated=models.DateTimeField(auto_now=True)  
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.body)
    

