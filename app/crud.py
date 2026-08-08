from sqlalchemy.orm import Session
from app import models, schemas
from uuid import UUID
from typing import Optional

def get_article_by_hash(db: Session, url_hash: str):
    return db.query(models.Article).filter(models.Article.url_hash == url_hash).first()

def create_article(db: Session, article_data: schemas.ArticleCreate):
    db_article = models.Article(**article_data.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def create_summary(db: Session, article_id: UUID, summary_data: dict):
    db_summary = models.Summary(
        article_id=article_id,
        tldr_bullets=summary_data.get("tldr_bullets", []),
        eli5_summary=summary_data.get("eli5_summary", "")
    )
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

def seed_initial_articles_if_empty(db: Session):
    if db.query(models.Article).count() == 0:
        import datetime
        import uuid
        categories = ["AI Research", "Tech News", "Startups", "Politics & Geopolitics", "Markets & Forex", "Tech News"]
        titles = [
            "AI Model Breakthrough: New Frontiers", 
            "Quantum Computing Hits New Milestone",
            "Top 10 Startups to Watch in 2026",
            "Global Geopolitics Shifts Towards Renewables",
            "Markets Rally Following Fed Announcement",
            "Next-Gen Smartphones Unveiled"
        ]
        now = datetime.datetime.utcnow()
        for i, cat_name in enumerate(categories):
            cat = db.query(models.Category).filter(models.Category.name == cat_name).first()
            if not cat:
                cat = models.Category(name=cat_name)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            
            article = models.Article(
                id=uuid.uuid4(),
                title=titles[i],
                original_url=f"https://example.com/seed-{i}",
                url_hash=f"seed_hash_{i}",
                published_at=now,
                category_id=cat.id,
                image_url=f"https://picsum.photos/seed/welcome{i}/800/450"
            )
            db.add(article)
            db.commit()
            
            summary = models.Summary(
                article_id=article.id,
                tldr_bullets=["This is a seeded article.", "Live feeds are currently being fetched.", "Refresh in a moment!"],
                eli5_summary="We seeded this placeholder article so your screen wouldn't be empty while the real news is fetching!"
            )
            db.add(summary)
            db.commit()
        return True
    return False

def get_articles(db: Session, skip: int = 0, limit: int = 20, category_id: Optional[int] = None, source_id: Optional[int] = None, search: Optional[str] = None, category: Optional[str] = None):
    query = db.query(models.Article)
    if category is not None and category.strip() != "" and category.lower() != "all":
        query = query.join(models.Category).filter(models.Category.name == category)
    elif category_id is not None:
        query = query.filter(models.Article.category_id == category_id)
    if source_id is not None:
        query = query.filter(models.Article.source_id == source_id)
    if search:
        query = query.filter(models.Article.title.ilike(f"%{search}%"))
    return query.order_by(models.Article.published_at.desc()).offset(skip).limit(limit).all()
