# 🚀 FastAPI Todo API

A modern, production-ready RESTful API built with **FastAPI** featuring user authentication, todo management, and clean architecture.

## ✨ Features

-   **🔐 JWT Authentication** - Secure user registration and login with OAuth2 password flow
-   **📝 Todo Management** - Full CRUD operations for todos with priority levels
-   **🛡️ Rate Limiting** - Protection against abuse with SlowAPI
-   **🐘 PostgreSQL** - Robust data persistence
-   **🐳 Docker Ready** - Easy deployment with Docker Compose
-   **📦 Clean Architecture** - Modular structure with separation of concerns

## 🛠️ Tech Stack

| Technology                                          | Purpose             |
| --------------------------------------------------- | ------------------- |
| [FastAPI](https://fastapi.tiangolo.com/)            | Web framework       |
| [SQLAlchemy](https://www.sqlalchemy.org/)           | ORM                 |
| [Alembic](https://alembic.sqlalchemy.org/)          | Database migrations |
| [PostgreSQL](https://www.postgresql.org/)           | Database            |
| [PyJWT](https://pyjwt.readthedocs.io/)              | JWT tokens          |
| [Passlib](https://passlib.readthedocs.io/) + bcrypt | Password hashing    |
| [SlowAPI](https://slowapi.readthedocs.io/)          | Rate limiting       |
| [Uvicorn](https://www.uvicorn.org/)                 | ASGI server         |

## 📁 Project Structure

```
src/
├── main.py              # Application entry point
├── api.py               # Route registration
├── exceptions.py        # Custom exception handlers
├── logging.py           # Logging configuration
├── rate_limiting.py     # Rate limiter setup
├── auth/                # Authentication module
│   ├── controller.py    # Auth endpoints
│   ├── model.py         # Pydantic schemas
│   └── service.py       # Auth business logic
├── todos/               # Todos module
│   ├── controller.py    # Todo endpoints
│   ├── model.py         # Pydantic schemas
│   └── service.py       # Todo business logic
├── users/               # Users module
│   ├── controller.py    # User endpoints
│   ├── model.py         # Pydantic schemas
│   └── service.py       # User business logic
├── entities/            # SQLAlchemy models
│   ├── todo.py          # Todo entity
│   └── user.py          # User entity
└── database/
    └── core.py          # Database configuration
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.14+
-   PostgreSQL 17+ (or Docker)
-   pip

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd FastAPI

# Start the application with Docker Compose
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Option 2: Local Development

1. **Clone and setup virtual environment**

```bash
git clone <repository-url>
cd FastAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cleanfastapi
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
```

4. **Start PostgreSQL** (if not using Docker)

```bash
# Make sure PostgreSQL is running and create the database
createdb cleanfastapi
```

5. **Run the application**

```bash
uvicorn src.main:app --reload
```

## 📚 API Endpoints

### Authentication

| Method | Endpoint      | Description              | Rate Limit |
| ------ | ------------- | ------------------------ | ---------- |
| `POST` | `/auth/`      | Register new user        | 5/hour     |
| `POST` | `/auth/token` | Login & get access token | -          |

### Users

| Method | Endpoint                 | Description              | Auth |
| ------ | ------------------------ | ------------------------ | ---- |
| `GET`  | `/users/me`              | Get current user profile | ✅   |
| `PUT`  | `/users/change-password` | Change password          | ✅   |

### Todos

| Method   | Endpoint                    | Description           | Auth |
| -------- | --------------------------- | --------------------- | ---- |
| `POST`   | `/todos/`                   | Create a new todo     | ✅   |
| `GET`    | `/todos/`                   | Get all user's todos  | ✅   |
| `GET`    | `/todos/{todo_id}`          | Get a specific todo   | ✅   |
| `PUT`    | `/todos/{todo_id}`          | Update a todo         | ✅   |
| `DELETE` | `/todos/{todo_id}`          | Delete a todo         | ✅   |
| `PUT`    | `/todos/{todo_id}/complete` | Mark todo as complete | ✅   |

## 📖 API Documentation

Once the server is running, access the interactive documentation:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔧 Environment Variables

| Variable       | Description                  | Example                               |
| -------------- | ---------------------------- | ------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `SECRET_KEY`   | JWT signing secret           | `your-secret-key`                     |
| `ALGORITHM`    | JWT algorithm                | `HS256`                               |

## 📊 Data Models

### User

```json
{
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
}
```

### Todo

```json
{
    "id": "uuid",
    "user_id": "uuid",
    "title": "My Todo",
    "description": "Todo description",
    "completed": false,
    "priority": "MEDIUM",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
}
```

**Priority Levels**: `LOW` (0), `MEDIUM` (1), `HIGH` (2)

## 🧪 Development

### Install dev dependencies

```bash
pip install -r requirements-dev.txt
```

### Run with hot reload

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
