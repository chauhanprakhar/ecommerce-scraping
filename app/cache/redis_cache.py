import json
import redis
from typing import Optional
from models import Product
from config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
    
    async def get_product(self, product_title: str) -> Optional[Product]:
        data = self.redis_client.get(product_title)
        if data:
            return Product(**json.loads(data))
        return None
    
    async def set_product(self, product: Product) -> None:
        self.redis_client.set(
            product.product_title,
            json.dumps(product.dict()),
            ex=3600
        )