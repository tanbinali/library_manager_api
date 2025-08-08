
# Library Manager API

A Django REST Framework based Library Management System API for managing books, members, and borrow records.  
Designed with role-based permissions to distinguish between librarians and members.

---

## Features

- **User Authentication** with JWT (Djoser + Simple JWT)
- **Role-Based Permissions**:
  - Librarians: Full CRUD on books, members, and borrow records.
  - Members: Can view books, borrow available books, and return borrowed books.
- **Borrow Records Management**:
  - Librarians manage all borrow records.
  - Members view only their active borrow records.
- **API Documentation** with Swagger and ReDoc (`/swagger/` and `/redoc/`).
- **Nested routing** for related resources like author’s books and member’s borrow records.

---

## Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Djoser (for user auth)
- Simple JWT (for token authentication)
- drf-yasg (for API documentation)
- PostgreSQL (or your preferred DB)
- Django Debug Toolbar (for debugging)

---

## Getting Started

### Prerequisites

- Python 3.10+
- Virtual environment tool (venv, pipenv, etc)
- Git

### Installation

1. Clone the repo  
```bash
git clone https://github.com/tanbinali/library_manager_api.git
cd library-manager
```

2. Create and activate a virtual environment  
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages  
```bash
pip install -r requirements.txt
```

4. Configure your database

* Edit `library_system/settings.py` to set up your database (default is SQLite, but you can configure PostgreSQL or others).

5. Apply database migrations  
```bash
python manage.py migrate
```

6. Create a superuser account (for admin access)  
```bash
python manage.py createsuperuser
```

7. Run the development server  
```bash
python manage.py runserver
```

8. Access the API documentation

* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Usage

- Use the admin panel (`/admin/`) to create user groups: **Librarian** and **Member**.
- Assign users to these groups accordingly.
- Librarians have full access to manage the library.
- Members can browse books, borrow available books, and return borrowed books through the API.

---

## API Endpoints Overview

- **Authentication:**

  - `POST /auth/users/` — Register a new user
  - `POST /auth/jwt/create/` — Obtain JWT token
  - `POST /auth/jwt/refresh/` — Refresh JWT token
  - `POST /auth/jwt/verify/` — Verify JWT token

- **Books:**

  - `GET /api/v1/books/` — List all books
  - `POST /api/v1/books/borrow/` — Borrow a book (members only)
  - `POST /api/v1/books/return_book/` — Return a borrowed book (members only)

- **Authors:**

  - Full CRUD for authors (librarians only)

- **Members:**

  - Full CRUD for members (librarians only)

- **Borrow Records:**

  - `GET /api/v1/records/` — View all borrow records (librarians only)
  - `GET /api/v1/records/mine/` — Members view their active borrow records

---

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit pull requests. For significant changes, open an issue first to discuss.

---

## License

This project is licensed under the MIT License.

---

## Contact

MD. Tanbin Ali  
Email: [tanbin@gmail.com](mailto:tanbin@gmail.com)  
GitHub: [https://github.com/tanbinali](https://github.com/tanbinali)

