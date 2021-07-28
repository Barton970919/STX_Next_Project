from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.TextField()
    authors = models.TextField()
    published_date = models.DateField(null=True)
    ISBN_10 = models.CharField(null=True, max_length=10)
    ISBN_13 = models.CharField(null=True, max_length=13)
    page_count = models.IntegerField(null=True)
    front_cover_link = models.URLField()
    language = models.CharField(max_length=10)
