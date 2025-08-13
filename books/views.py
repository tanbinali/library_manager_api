from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    
    def get_permissions(self):
        """
        Assign different permissions depending on the action.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['borrow', 'return_book']:
            permission_classes = [IsAuthenticated, IsMemberGroupOnly]
        else:
            permission_classes = [IsLibrarianOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'borrow':
            return BookBorrowSerializer
        if self.action == 'return_book':
            return BookReturnSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_summary="List all books",
        operation_description="Retrieve a list of all books with author details.",
        responses={200: BookSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a book",
        operation_description="Retrieve details of a specific book by ID.",
        responses={200: BookSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new book",
        operation_description="Add a new book to the library (librarians/admins only).",
        request_body=BookSerializer,
        responses={201: BookSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a book",
        operation_description="Fully update a book record (librarians/admins only).",
        request_body=BookSerializer,
        responses={200: BookSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a book",
        operation_description="Partially update a book record (librarians/admins only).",
        request_body=BookSerializer,
        responses={200: BookSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a book",
        operation_description="Delete a book from the library (librarians/admins only).",
        responses={204: 'No Content'},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        request_body=BookBorrowSerializer,
        operation_summary="Borrow a book",
        operation_description="Allows members to borrow a book by its title. Book must be available.",
        responses={
            201: openapi.Response(description="Successfully borrowed the book."),
            400: "Book not available or invalid title.",
        },
    )
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

    @swagger_auto_schema(
        method='post',
        request_body=BookReturnSerializer,
        operation_summary="Return a book",
        operation_description="Allows members to return a previously borrowed book by title.",
        responses={
            200: openapi.Response(description="Successfully returned the book."),
            400: "No active borrow record found for this book.",
        },
    )
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

    def get_permissions(self):
        from rest_framework.permissions import SAFE_METHODS

        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsLibrarianGroupOrReadOnly(), IsAdminUser()]

    @swagger_auto_schema(
        operation_summary="List authors",
        operation_description="Retrieve a list of all authors.",
        responses={200: AuthorSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve author",
        operation_description="Get details of a specific author by ID.",
        responses={200: AuthorSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create author",
        operation_description="Add a new author (librarians/admins only).",
        request_body=AuthorSerializer,
        responses={201: AuthorSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update author",
        operation_description="Fully update an author (librarians/admins only).",
        request_body=AuthorSerializer,
        responses={200: AuthorSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update author",
        operation_description="Partially update an author (librarians/admins only).",
        request_body=AuthorSerializer,
        responses={200: AuthorSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete author",
        operation_description="Delete an author (librarians/admins only).",
        responses={204: 'No Content'},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
