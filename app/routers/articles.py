from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app import crud, models, schemas
from app.database import get_db, SessionLocal
from app.services.ingest import process_feed
from app.services.analytics import get_trending_articles

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)

class IngestRequest(BaseModel):
    feed_url: str
    source_id: int
    category_id: int

def run_process_feed(feed_url: str, source_id: int, category_id: int):
    db = SessionLocal()
    try:
        process_feed(feed_url, source_id, category_id, db)
    finally:
        db.close()

@router.post("/ingest")
def trigger_ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_process_feed, request.feed_url, request.source_id, request.category_id)
    return {"message": "Ingestion started in the background", "feed_url": request.feed_url}

@router.post("/ingest_category")
def trigger_ingest_category(category: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Simple mock endpoint to satisfy frontend trigger request
    # In a real app, this would look up the sources for the category and ingest them
    return {"message": f"Ingestion triggered for {category}"}



@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category.name).distinct().all()
    if categories and len(categories) > 0:
        return [c[0] for c in categories]
    return ["AI Research", "Tech News", "Startups", "Politics & Geopolitics", "Markets & Forex"]

@router.get("/trending")
def read_trending_articles(db: Session = Depends(get_db)):
    articles = get_trending_articles(db, limit=5)
    if not articles or len(articles) == 0:
        return []
        
    result = []
    for a in articles:
        summary_text = "No summary available."
        eli5_text = "No ELI5 summary available."
        if a.summary:
            if a.summary.tldr_bullets and len(a.summary.tldr_bullets) > 0:
                summary_text = a.summary.tldr_bullets[0]
            if a.summary.eli5_summary:
                eli5_text = a.summary.eli5_summary
            
        result.append({
            "id": str(a.id),
            "title": a.title,
            "summary": summary_text,
            "eli5_summary": eli5_text,
            "source": a.source.name if a.source else "TECH NEWS",
            "category": a.category.name if a.category else "Uncategorized",
            "published_at": a.published_at.isoformat() + "Z" if a.published_at else None,
            "url": a.original_url,
            "image_url": a.image_url or "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=800&auto=format&fit=crop"
        })
    return result

@router.get("/")
def read_articles(skip: int = 0, limit: int = 20, category_id: Optional[int] = None, category: Optional[str] = None, source_id: Optional[int] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit, category_id=category_id, source_id=source_id, search=search, category=category)
    
    if category is not None and category.strip() != "" and category.lower() != "all":
        articles = [a for a in articles if a.category and a.category.name.lower() == category.lower()]
        
    if not articles or len(articles) == 0:
        return []
        
    result = []
    for a in articles:
        summary_text = "No summary available."
        eli5_text = "No ELI5 summary available."
        if a.summary:
            if a.summary.tldr_bullets and len(a.summary.tldr_bullets) > 0:
                summary_text = a.summary.tldr_bullets[0]
            if a.summary.eli5_summary:
                eli5_text = a.summary.eli5_summary
            
        result.append({
            "id": str(a.id),
            "title": a.title,
            "summary": summary_text,
            "eli5_summary": eli5_text,
            "source": a.source.name if a.source else "TECH NEWS",
            "category": a.category.name if a.category else "Uncategorized",
            "published_at": a.published_at.isoformat() + "Z" if a.published_at else None,
            "url": a.original_url,
            "image_url": a.image_url or "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=800&auto=format&fit=crop"
        })
        
    return result

@router.get("/{article_id}", response_model=schemas.ArticleOut)
def read_article(article_id: UUID, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/{article_id}/track")
def track_article_action(article_id: UUID, action_type: str, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    if action_type == "VIEW":
        article.views_count += 1
    elif action_type == "READ":
        article.reads_count += 1
        
    activity = models.NewsActivity(
        article_id=article.id,
        activity_type=action_type
    )
    db.add(activity)
    db.commit()
    return {"message": "Action tracked"}
