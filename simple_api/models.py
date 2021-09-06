from django.db import models



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

