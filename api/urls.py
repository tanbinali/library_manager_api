from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from books.views import BookViewSet, AuthorViewSet
from members.views import MemberViewSet, BorrowRecordViewSet

# Main routers
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'members', MemberViewSet, basename='members')
router.register(r'records', BorrowRecordViewSet, basename='records')

# Nested routers
author_books_router = NestedDefaultRouter(router, r'authors', lookup='author')
author_books_router.register(r'books', BookViewSet, basename='author-books')

member_records_router = NestedDefaultRouter(router, r'members', lookup='member')
member_records_router.register(r'records', BorrowRecordViewSet, basename='member-records')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(author_books_router.urls)),
    path('', include(member_records_router.urls)),
]
