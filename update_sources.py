import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Summary, Article, Source, Category

db = SessionLocal()

# Clear out old cached articles, summaries, sources, categories
db.query(Summary).delete()
db.query(Article).delete()
db.query(Source).delete()
db.query(Category).delete()

categories = ["AI Research", "Tech News", "Startups", "Politics & Geopolitics", "Markets & Forex"]
for i, name in enumerate(categories, 1):
    db.add(Category(id=i, name=name))

# Add live Google News RSS feeds
db.add(Source(name="Tech/AI Google News", url="https://news.google.com/rss/search?q=technology+AI&hl=en-US&gl=US&ceid=US:en"))
db.add(Source(name="Global Google News", url="https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"))

db.commit()
db.close()
print("Database cleared. Standardized categories and new RSS feeds configured.")
