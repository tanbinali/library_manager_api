# populate_db.py

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')  # adjust if your settings module is different
django.setup()

from books.models import Author, Book

def populate():
    authors_data = [
        {
            "name": "J.K. Rowling",
            "biography": "British author, best known for the Harry Potter series."
        },
        {
            "name": "George Orwell",
            "biography": "English novelist and essayist, famous for '1984' and 'Animal Farm'."
        },
        {
            "name": "Jane Austen",
            "biography": "English novelist known primarily for her six major novels including 'Pride and Prejudice'."
        }
    ]

    books_data = [
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "author_name": "J.K. Rowling",
            "ISBN": "9780439708180",
            "category": "Fantasy",
            "availability": True
        },
        {
            "title": "1984",
            "author_name": "George Orwell",
            "ISBN": "9780451524935",
            "category": "Dystopian",
            "availability": True
        },
        {
            "title": "Animal Farm",
            "author_name": "George Orwell",
            "ISBN": "9780451526342",
            "category": "Political Satire",
            "availability": True
        },
        {
            "title": "Pride and Prejudice",
            "author_name": "Jane Austen",
            "ISBN": "9780141040349",
            "category": "Classic Romance",
            "availability": True
        }
    ]

    # Create authors
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(name=author_data["name"], defaults={"biography": author_data["biography"]})
        if created:
            print(f"Created author: {author.name}")
        else:
            print(f"Author already exists: {author.name}")

    # Create books
    for book_data in books_data:
        author = Author.objects.get(name=book_data["author_name"])
        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            defaults={
                "author": author,
                "ISBN": book_data["ISBN"],
                "category": book_data["category"],
                "availability": book_data["availability"],
            }
        )
        if created:
            print(f"Created book: {book.title}")
        else:
            print(f"Book already exists: {book.title}")

if __name__ == '__main__':
    populate()
