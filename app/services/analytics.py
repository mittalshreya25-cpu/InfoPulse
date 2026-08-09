from sqlalchemy.orm import Session
from app.models import Article

def get_trending_articles(db: Session, limit: int = 5):
    """
    Returns the top trending articles based on engagement score: (views_count * 1 + reads_count * 3).
    If there aren't enough trending articles with activity, it falls back to the most recently published articles.
    """
    trending_articles = db.query(Article).filter(
        (Article.views_count > 0) | (Article.reads_count > 0)
    ).order_by(
        (Article.views_count * 1 + Article.reads_count * 3).desc()
    ).limit(limit).all()
    
    if len(trending_articles) < limit:
        existing_ids = [a.id for a in trending_articles]
        needed = limit - len(trending_articles)
        fallback_articles = db.query(Article).filter(
            Article.id.notin_(existing_ids)
        ).order_by(Article.published_at.desc()).limit(needed).all()
        
        trending_articles.extend(fallback_articles)
        
    return trending_articles
