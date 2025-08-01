from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    ISBN = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title
