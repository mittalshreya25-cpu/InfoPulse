import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models import Source, Category
from app.services.ingest import process_feed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORIES = ["AI Research", "Tech News", "Startups", "Politics & Geopolitics", "Markets & Forex"]

SOURCES = [
    # AI Research
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/feed/", "category": "AI Research"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "AI Research"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "category": "AI Research"},
    
    # Tech News
    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "category": "Tech News"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "category": "Tech News"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "Tech News"},
    
    # Startups
    {"name": "TechCrunch Startups", "url": "https://techcrunch.com/category/startups/feed/", "category": "Startups"},
    
    # Politics & Geopolitics
    {"name": "Reuters World News", "url": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best", "category": "Politics & Geopolitics"},
    {"name": "NDTV India News", "url": "https://feeds.feedburner.com/ndtvnews-india-news", "category": "Politics & Geopolitics"},
    {"name": "BBC World News", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "category": "Politics & Geopolitics"},
    
    # Markets & Forex
    {"name": "Economic Times Markets", "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "category": "Markets & Forex"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/news/rssindex", "category": "Markets & Forex"}
]

def seed():
    # Clear mismatched records by resetting the schema
    logger.info("Dropping and recreating database schema to clear old mismatched records...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database reset complete.")
    
    db = SessionLocal()
    
    try:
        # 1. Seed Categories
        category_map = {}
        for cat_name in CATEGORIES:
            category = db.query(Category).filter(Category.name == cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.add(category)
                db.commit()
                db.refresh(category)
                logger.info(f"Added category: {cat_name}")
            category_map[cat_name] = category.id

        # 2. Seed Sources
        for src_data in SOURCES:
            source = db.query(Source).filter(Source.url == src_data["url"]).first()
            if not source:
                source = Source(name=src_data["name"], url=src_data["url"])
                db.add(source)
                db.commit()
                db.refresh(source)
                logger.info(f"Added source: {src_data['name']}")

        # 3. Run Ingestion for all sources
        logger.info("Starting feed ingestion for all sources...")
        all_sources = db.query(Source).all()
        for source in all_sources:
            target_cat_name = "AI Research"
            for s in SOURCES:
                if s["url"] == source.url:
                    target_cat_name = s["category"]
                    break
            
            # Default to first category if not found
            cat_id = category_map.get(target_cat_name, list(category_map.values())[0])
            
            logger.info(f"Ingesting {source.name} ({source.url})...")
            process_feed(source.url, source.id, cat_id, db)
            
        logger.info("Seed and ingestion complete!")
        
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
