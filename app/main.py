from fastapi import FastAPI
from app.db.base import Base, engine
from app.api.routes import auth, expenses

app = FastAPI(
    title="Expense Tracker API",
    version="0.1.0",
    description=(
        "Simple authenticated API for tracking personal expenses.\n\n"
        "- Users sign up and log in.\n"
        "- JWT protects all expense routes.\n"
        "- Supports CRUD operations and time-based filtering."
    ),
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}