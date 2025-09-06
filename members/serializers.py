from rest_framework import serializers
from .models import Member, BorrowRecord
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for Member model.

    Serializes basic member information:
    - id: Unique identifier.
    - username: User's username.
    - email: User's email address.
    - membership_date: Date when the member joined.
    """
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'membership_date']


class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for BorrowRecord model.

    Read-only fields:
    - member: String representation of the member who borrowed the book.
    - book: String representation of the borrowed book.

    Write-only fields:
    - book_id: Primary key for selecting the book to borrow.

    Fields:
    - id: Unique identifier for the borrow record.
    - borrowed_at: Timestamp when the book was borrowed.
    - returned_at: Timestamp when the book was returned (nullable).
    """
    member = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.select_related('author').all(),  # Optimization: prefetch author if needed
        write_only=True,
        source='book'
    )

    class Meta:
        model = BorrowRecord
        fields = ['id', 'member', 'book', 'book_id', 'borrowed_at', 'returned_at']
        read_only_fields = ['id', 'member', 'borrowed_at', 'returned_at']


class MemberCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new User accounts.

    Handles user registration by accepting username, email,
    password (write-only), first name, and last name.

    Password is hashed before saving the user.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for User model to retrieve user details.

    Provides:
    - id: User ID.
    - username: User's username.
    - email: User's email.
    - first_name: User's first name.
    - last_name: User's last name.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
