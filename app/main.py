from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models
from app.database import engine, get_db, SessionLocal
from app.routers import articles, finance
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.ingest import process_feed, ingest_latest_news

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute on startup
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://infopulselive.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(finance.router)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")



@app.on_event("startup")
def start_scheduler():
    import threading
    from app.crud import seed_initial_articles_if_empty
    
    # Run immediate initial database seeding
    db = SessionLocal()
    try:
        seed_initial_articles_if_empty(db)
    finally:
        db.close()
    
    # Trigger immediately on startup
    threading.Thread(target=ingest_latest_news, daemon=True).start()
    
    # Run background scheduler every 10 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(ingest_latest_news, 'interval', minutes=10)
    scheduler.start()
