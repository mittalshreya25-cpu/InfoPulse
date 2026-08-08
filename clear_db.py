import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Summary, Article

db = SessionLocal()
db.query(Summary).delete()
db.query(Article).delete()
db.commit()
db.close()
print("Cleared summaries and articles tables.")
