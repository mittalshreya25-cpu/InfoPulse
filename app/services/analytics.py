from sqlalchemy.orm import Session
from app.models import Article

def get_trending_articles(db: Session, limit: int = 5):
    """
    Returns the top trending articles based on engagement score: (views_count * 1 + reads_count * 3).
    Only returns articles that have at least some activity (views or reads).
    """
    trending_articles = db.query(Article).filter(
        (Article.views_count > 0) | (Article.reads_count > 0)
    ).order_by(
        (Article.views_count * 1 + Article.reads_count * 3).desc()
    ).limit(limit).all()
    
    return trending_articles
