from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Serializes all fields of the Author model.
    Used to represent author details within book objects as nested data.
    """
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    - Includes nested representation of the author using AuthorSerializer (read-only).
    - Allows setting the author by ID via the `author_id` write-only field.
    - Serializes book details including title, ISBN, category, and availability status.

    Fields:
    - id: Unique identifier of the book.
    - title: Title of the book.
    - author: Nested author details (read-only).
    - author_id: Primary key of the author (write-only).
    - ISBN: Book's ISBN number.
    - category: Category or genre of the book.
    - availability: Boolean indicating if the book is available for borrowing.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True,
        source='author'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'ISBN', 'category', 'availability']
