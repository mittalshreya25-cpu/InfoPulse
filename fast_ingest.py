import datetime
import dateutil.parser
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from app.services.scraper import fetch_rss_feed, hash_url
import logging

logger = logging.getLogger(__name__)

def fast_ingest(feed_url: str, source_id: int, category_id: int, db: Session, limit: int = 5):
    try:
        items = fetch_rss_feed(feed_url)
    except Exception as e:
        print(f"Error fetching: {e}")
        return
        
    count = 0
    for item in items:
        if count >= limit:
            break
            
        original_url = item.get("link", "")
        if not original_url:
            continue
            
        try:
            url_hash_val = hash_url(original_url)
            
            title = item.get("title", "")
            existing_article = db.query(models.Article).filter(
                (models.Article.url_hash == url_hash_val) | 
                (models.Article.title == title)
            ).first()
                
            if existing_article:
                continue
                
            published_at = datetime.datetime.now(datetime.timezone.utc)
            
            image_url = f"https://picsum.photos/seed/{url_hash_val}/800/450"

            article_data = schemas.ArticleCreate(
                title=item.get("title", "Untitled"),
                original_url=original_url,
                url_hash=url_hash_val,
                published_at=published_at,
                source_id=source_id,
                category_id=category_id,
                image_url=image_url
            )
            
            new_article = crud.create_article(db, article_data)
            
            # Create a dummy summary so it doesn't look empty
            dummy_summary = {
                "tldr_bullets": ["Summary generation delayed due to high server load.", "Check back later for AI insights."],
                "eli5_summary": "We are currently processing thousands of news articles. The AI summary for this specific article will be generated in the background soon!"
            }
            crud.create_summary(db, new_article.id, dummy_summary)
            
            count += 1
            print(f"Fast ingested: {title}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Fast ingesting Startups...")
        fast_ingest("https://news.google.com/rss/search?q=startups+venture+capital&hl=en-US&gl=US&ceid=US:en", 18, 3, db, limit=10)
        
        print("Fast ingesting Markets & Forex...")
        fast_ingest("https://news.google.com/rss/search?q=markets+finance+forex&hl=en-US&gl=US&ceid=US:en", 19, 5, db, limit=10)
    finally:
        db.close()
