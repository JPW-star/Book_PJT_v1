from django.db import models

class Book(models.Model):
    isbn13 = models.CharField(max_length=13, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    cover = models.URLField()
    descriptions = models.TextField()

    def __str__(self):
        return self.title
