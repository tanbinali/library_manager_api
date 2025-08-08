from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone

from books.models import Book
from books.serializers import BookSerializer
from members.models import BorrowRecord
from api.permissions import (
    IsLibrarianOrAdminOrReadOnly,
    IsMemberGroupOnly,
    IsLibrarianGroupOrReadOnly
)
from .models import Author
from .serializers import AuthorSerializer


class BookBorrowSerializer(serializers.Serializer):
    """
    Serializer used for borrowing a book via its title.
    """
    title = serializers.SlugRelatedField(
        queryset=Book.objects.filter(availability=True),
        slug_field='title'
    )


class BookReturnSerializer(serializers.Serializer):
    """
    Serializer used for returning a book via its title.
    """
    title = serializers.SlugRelatedField(
        queryset=Book.objects.all(),
        slug_field='title'
    )


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.

    Permissions:
    - Librarians and Admins have full CRUD access.
    - Members can borrow and return books using custom endpoints.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'borrow':
            return BookBorrowSerializer
        if self.action == 'return_book':
            return BookReturnSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsMemberGroupOnly])
    def borrow(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data['title']

        if not book.availability:
            return Response({"detail": "Book is currently not available."}, status=status.HTTP_400_BAD_REQUEST)

        BorrowRecord.objects.create(
            member=request.user,
            book=book,
            borrowed_at=timezone.now()
        )
        book.availability = False
        book.save()

        return Response({"detail": f"You have borrowed '{book.title}'."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsMemberGroupOnly])
    def return_book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data['title']

        try:
            record = BorrowRecord.objects.get(
                member=request.user,
                book=book,
                returned_at__isnull=True
            )
        except BorrowRecord.DoesNotExist:
            return Response({"detail": "You do not have an active borrow record for this book."},
                            status=status.HTTP_400_BAD_REQUEST)

        record.returned_at = timezone.now()
        record.save()

        book.availability = True
        book.save()

        return Response({"detail": f"You have returned '{book.title}'."}, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing authors.

    Permissions:
    - Authenticated users can view author details.
    - Only librarians and admins can create, update, or delete authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # Combined permission so that:
    # - ReadOnly for authenticated users
    # - Write allowed only for Librarian group or Admin users
    def get_permissions(self):
        from rest_framework.permissions import SAFE_METHODS

        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsLibrarianGroupOrReadOnly(), IsAdminUser()]
