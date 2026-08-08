import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://newsuser:newspassword@localhost:5432/newsdb")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE articles ADD COLUMN views_count INTEGER DEFAULT 0;"))
            print("Added views_count to articles")
        except Exception as e:
            print("views_count already exists or error:", e)
            
        try:
            conn.execute(text("ALTER TABLE articles ADD COLUMN reads_count INTEGER DEFAULT 0;"))
            print("Added reads_count to articles")
        except Exception as e:
            print("reads_count already exists or error:", e)
            
        try:
            conn.execute(text("ALTER TABLE news_activity RENAME COLUMN action_type TO activity_type;"))
            print("Renamed action_type to activity_type in news_activity")
        except Exception as e:
            print("activity_type already renamed or error:", e)
            
        try:
            conn.execute(text("ALTER TABLE news_activity RENAME COLUMN created_at TO timestamp;"))
            print("Renamed created_at to timestamp in news_activity")
        except Exception as e:
            print("timestamp already renamed or error:", e)
            
        try:
            conn.execute(text("ALTER TABLE news_activity ALTER COLUMN timestamp TYPE TIMESTAMP WITH TIME ZONE;"))
            print("Altered timestamp type to TIMESTAMP WITH TIME ZONE")
        except Exception as e:
            print("timestamp type already altered or error:", e)

        conn.commit()
        print("Migration complete.")

if __name__ == "__main__":
    run_migration()
