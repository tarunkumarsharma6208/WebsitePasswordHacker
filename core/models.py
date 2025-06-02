from django.db import models

# Create your models here.

class UserPassword(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    try_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.username}'