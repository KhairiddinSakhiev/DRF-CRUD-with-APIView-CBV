from django.db import models
from accounts.models import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish a post")
        ]


class Author(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    title = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pages = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
