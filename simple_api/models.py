from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey



class Category(models.Model):
    name = models.CharField(max_length=255)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



class Book(models.Model):
    title =  models.CharField(max_length=255)
    release_year = models.IntegerField()
    rating = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


from django.contrib.auth import get_user_model

User = get_user_model()

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

