from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'ISBN', 'category', 'availability']
