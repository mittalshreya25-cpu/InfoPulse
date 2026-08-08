import uuid
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship  # pyrefly: ignore [missing-import]
from app.database import Base
from datetime import datetime, timezone

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String)

    articles = relationship("Article", back_populates="source")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    original_url = Column(String)
    url_hash = Column(String, unique=True, index=True)
    published_at = Column(DateTime)
    source_id = Column(Integer, ForeignKey("sources.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String, nullable=True)
    views_count = Column(Integer, default=0)
    reads_count = Column(Integer, default=0)

    source = relationship("Source", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    summary = relationship("Summary", back_populates="article", uselist=False)

    @property
    def url(self):
        return self.original_url
        
    @property
    def eli5_summary(self):
        return self.summary.eli5_summary if self.summary else None

class NewsActivity(Base):
    __tablename__ = "news_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"))
    activity_type = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    article = relationship("Article")

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), unique=True)
    tldr_bullets = Column(JSONB)
    eli5_summary = Column(String)

    article = relationship("Article", back_populates="summary")