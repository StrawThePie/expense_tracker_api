# Expense Tracker API

Backend API for tracking personal expenses.

Created for https://roadmap.sh/projects/expense-tracker-api

## Features

- User registration and login with JWT authentication.
- CRUD operations on expenses scoped to the authenticated user.
- Filtering by past week, past month, last 3 months, or custom date range.
- Pagination with `limit` and `offset` query parameters on the expenses list.

## Tech Stack

- Python & FastAPI
- PostgreSQL with SQLAlchemy
- JWT auth using `python-jose`
- Alembic for migrations (optional)

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
    ```

3. Copy ```.env.example``` to ```.env``` and set your values (database URL, JWT secret, etc.).
4. Run the app:
    
    ```bash
    uvicorn app.main:app --reload
    ```
   
5. Open http://127.0.0.1:8000/docs to explore the API.