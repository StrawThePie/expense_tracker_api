from fastapi import FastAPI
from app.db.base import Base, engine
from app.api.routes import auth, expenses

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}