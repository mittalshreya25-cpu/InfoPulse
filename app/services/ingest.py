import datetime
import logging
import dateutil.parser
from sqlalchemy.orm import Session

from app import crud, schemas
from app.services.scraper import fetch_rss_feed, extract_clean_text, hash_url
from app.services.summarizer import generate_summary

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_feed(feed_url: str, source_id: int, category_id: int, db: Session):
    """
    Process an RSS feed: fetch articles, deduplicate, scrape text, summarize, and save.
    """
    try:
        items = fetch_rss_feed(feed_url)
    except Exception as e:
        logger.error(f"Error fetching RSS feed {feed_url}: {e}")
        return {"status": "error", "message": str(e)}
        
    new_articles_count = 0
    
    for item in items:
        original_url = item.get("link", "")
        if not original_url:
            continue
            
        try:
            url_hash_val = hash_url(original_url)
            
            # Check if article already exists
            from app import models
            title = item.get("title", "")
            
            if title:
                existing_article = db.query(models.Article).filter(
                    (models.Article.url_hash == url_hash_val) | 
                    (models.Article.title == title)
                ).first()
            else:
                existing_article = crud.get_article_by_hash(db, url_hash_val)
                
            if existing_article:
                continue
                
            # Parse published date and convert to UTC datetime
            published_at = None
            published_str = item.get("published", "")
            if published_str:
                try:
                    dt = dateutil.parser.parse(published_str)
                    published_at = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                except Exception as e:
                    logger.warning(f"Error parsing date {published_str} for {original_url}: {e}")
            
            if not published_at:
                published_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                    
            # Scrape full text, fallback to RSS summary if scraping fails
            try:
                full_text = extract_clean_text(original_url)
            except Exception as e:
                logger.error(f"Error scraping text for {original_url}: {e}")
                full_text = ""
                
            # Get safe summary string
            item_summary = item.get('summary', item.get('description', item.get('subtitle', '')))
            if not item_summary and 'content' in item and len(item.content) > 0:
                item_summary = item.content[0].get('value', '')
                
            if item_summary and not isinstance(item_summary, str):
                item_summary = str(item_summary)

            text_to_summarize = full_text if full_text else item_summary
            
            if not text_to_summarize:
                logger.warning(f"No text to summarize for {original_url}")
                continue
                
            # Extract image from RSS feed
            image_url = None
            if "media_content" in item and item.media_content:
                image_url = item.media_content[0].get("url")
            elif "media_thumbnail" in item and item.media_thumbnail:
                image_url = item.media_thumbnail[0].get("url")
            elif "enclosures" in item and item.enclosures:
                for enc in item.enclosures:
                    if enc.get("type", "").startswith("image/"):
                        image_url = enc.get("href")
                        break
            
            if not image_url and item_summary:
                import re
                img_match = re.search(r'<img[^>]+src="([^">]+)"', item_summary)
                if img_match:
                    image_url = img_match.group(1)
                    
            if not image_url:
                image_url = f"https://picsum.photos/seed/{url_hash_val}/800/450"

            # Create article record
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
            
            # Generate summary using Gemini
            try:
                summary_data = generate_summary(text_to_summarize)
                if summary_data:
                    crud.create_summary(db, new_article.id, summary_data)
                else:
                    logger.warning(f"Summary generation returned None for {original_url}")
            except Exception as e:
                logger.error(f"Error generating summary for {original_url}: {e}")
            
            new_articles_count += 1
        except Exception as e:
            logger.error(f"Unexpected error processing article {original_url}: {e}")
            continue
            
    return {"status": "success", "processed_feed": feed_url, "new_articles_added": new_articles_count}

def ingest_latest_news():
    from app.database import SessionLocal
    from app import models
    db = SessionLocal()
    try:
        sources = db.query(models.Source).all()
        for source in sources:
            if source.url:
                cat_id = 1
                cat = db.query(models.Category).filter(models.Category.name == source.name).first()
                if cat:
                    cat_id = cat.id
                else:
                    if "AI" in source.name:
                        cat = db.query(models.Category).filter(models.Category.name == "AI Research").first()
                        if cat: cat_id = cat.id
                    else:
                        cat = db.query(models.Category).filter(models.Category.name == "Politics & Geopolitics").first()
                        if cat: cat_id = cat.id
                process_feed(source.url, source.id, cat_id, db)
    except Exception as e:
        logger.error(f"Error during scheduled feed ingestion: {e}")
    finally:
        db.close()
