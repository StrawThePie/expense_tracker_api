from fastapi import FastAPI
from app.api.routes import auth
from app.db.base import Base, engine

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}