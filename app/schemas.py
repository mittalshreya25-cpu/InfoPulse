from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class SourceBase(BaseModel):
    name: str
    url: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class SourceOut(SourceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class SummaryOut(BaseModel):
    tldr_bullets: List[str]
    eli5_summary: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ArticleBase(BaseModel):
    title: str
    original_url: str
    url_hash: str
    published_at: Optional[datetime] = None
    source_id: Optional[int] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleOut(ArticleBase):
    id: UUID
    source: Optional[SourceOut] = None
    category: Optional[CategoryOut] = None
    summary: Optional[SummaryOut] = None

    model_config = ConfigDict(from_attributes=True)
