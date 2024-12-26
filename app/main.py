from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from typing import List
import asyncio
import sys
from pathlib import Path

src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from app.scraper.scraper import Scraper
from app.models.models import Product, ScrapingSettings
from storage.json_storage import JsonStorage
from notifications.console import ConsoleNotification
from cache.redis_cache import RedisCache
from config import settings

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

@app.post("/scrape/", response_model=List[Product])
async def scrape_products(
    scraping_settings: ScrapingSettings,
    api_key: str = Depends(get_api_key)
):
    target_url = scraping_settings.target_url or settings.DEFAULT_TARGET_URL
    scraper = Scraper(str(target_url))
    storage = JsonStorage()
    cache = RedisCache()
    notifier = ConsoleNotification()
    
    all_products = []
    updated_products = 0
    
    max_pages = scraping_settings.page_limit or float('inf')
    page = 1
    
    while page <= max_pages:
        try:
            products = await scraper.scrape_page(page, scraping_settings)
            if not products:
                break
                
            for product in products:
                cached_product = await cache.get_product(product.product_title)
                if not cached_product or cached_product.product_price != product.product_price:
                    all_products.append(product)
                    await cache.set_product(product)
                    updated_products += 1
                    
            page += 1
        except Exception as e:
            await notifier.notify(f"Error scraping page {page}: {str(e)}")
            break
    
    if all_products:
        await storage.save_products(all_products)
    
    await notifier.notify(
        f"Scraping completed: {len(all_products)} products found, {updated_products} products updated"
    )
    
    return all_products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)