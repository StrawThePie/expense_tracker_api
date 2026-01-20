# Expense Tracker API

Backend API for tracking personal expenses

## Features

- User registration and login with JWT authentication.
- CRUD operations on expenses scoped to the authenticated user.
- Filtering by past week, past month, last 3 months, or custom date range.
- Pagination with `limit` and `offset` query parameters on the expenses list.[web:69]

## Tech Stack

- Python & FastAPI
- PostgreSQL with SQLAlchemy
- JWT auth using `python-jose`
- Alembic for migrations (optional)[web:95]

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
