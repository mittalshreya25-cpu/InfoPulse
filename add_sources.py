import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app import models

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://newsuser:newspassword@localhost:5432/newsdb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_missing_sources():
    db = SessionLocal()
    try:
        sources_to_add = [
            ("Tech News", "https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en"),
            ("Startups", "https://news.google.com/rss/search?q=startups+venture+capital&hl=en-US&gl=US&ceid=US:en"),
            ("Markets & Forex", "https://news.google.com/rss/search?q=markets+finance+forex&hl=en-US&gl=US&ceid=US:en")
        ]
        
        for name, url in sources_to_add:
            existing = db.query(models.Source).filter(models.Source.name == name).first()
            if not existing:
                new_source = models.Source(name=name, url=url)
                db.add(new_source)
                print(f"Added source: {name}")
            else:
                print(f"Source {name} already exists.")
        
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_sources()
