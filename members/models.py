from django.contrib.auth.models import AbstractUser
from django.db import models
from books.models import Book
from django.db import models
from django.conf import settings
from django.utils import timezone

class Member(AbstractUser):
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class BorrowRecord(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} borrowed {self.book} at {self.borrowed_at}"