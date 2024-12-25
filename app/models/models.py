from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ScrapingSettings(BaseModel):
    page_limit: Optional[int] = None
    proxy: Optional[str] = None
    target_url: Optional[HttpUrl] = None  # Added target URL field

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
