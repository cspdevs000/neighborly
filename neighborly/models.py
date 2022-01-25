from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    address = models.CharField(max_length=100)
    number_of_apts = models.IntegerField(default=0)
    def __str__(self):
        return self.address

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.body

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.body