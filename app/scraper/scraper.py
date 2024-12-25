import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Optional
import os
from models import Product, ScrapingSettings
from config import settings

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        
    async def _download_image(self, image_url: str, product_title: str) -> str:
        async with httpx.AsyncClient() as client:
            # Handle relative URLs
            if image_url.startswith('/'):
                image_url = f"{self.base_url}{image_url}"
            elif not image_url.startswith(('http://', 'https://')):
                image_url = f"{self.base_url}/{image_url}"
                
            response = await client.get(image_url)
            if response.status_code == 200:
                os.makedirs("images", exist_ok=True)
                safe_filename = "".join(x for x in product_title if x.isalnum() or x in (' ','-','_')).rstrip()
                image_path = f"images/{safe_filename}.jpg"
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                return image_path
            return ""

    async def _fetch_page_with_retry(self, url: str, proxy: Optional[str] = None) -> str:
        for attempt in range(settings.RETRY_ATTEMPTS):
            try:
                async with httpx.AsyncClient(
                    proxies={"all://": proxy} if proxy else None,
                    follow_redirects=True,
                    timeout=30.0
                ) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.text
            except httpx.HTTPError as e:
                if attempt < settings.RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(settings.RETRY_DELAY)
                else:
                    raise Exception(f"Failed to fetch page after {settings.RETRY_ATTEMPTS} attempts: {str(e)}")
    
    async def scrape_page(self, page_number: int, scraping_settings: ScrapingSettings) -> List[Product]:
        # For dentalstall.com, adjust the URL pattern according to their pagination structure
        url = f"{self.base_url}/page/{page_number}/" if page_number > 1 else self.base_url
        html = await self._fetch_page_with_retry(url, scraping_settings.proxy)
        soup = BeautifulSoup(html, 'html.parser')
        
        products = []
        print("url" + url)
        # Updated selectors for dentalstall.com
        for product_elem in soup.select('li.product'):
            try:
                title_elem = product_elem.select_one('h2.woo-loop-product__title')
                price_elem = product_elem.select_one('span.price')
                image_elem = product_elem.select_one('img.attachment-woocommerce_thumbnail')
                # print(image_elem)
                if title_elem and price_elem and image_elem:
                    title = title_elem.text.strip()
                    # Handle different price formats (regular, sale)
                    price_text = price_elem.select_one('span.amount').text.strip()
                    price = float(price_text.replace('₹', '').replace(',', '').strip())
                    image_url = image_elem.get('data-lazy-src', '')
                    # print(image_url)
                    image_path = await self._download_image(image_url, title)
                    
                    products.append(Product(
                        product_title=title,
                        product_price=price,
                        path_to_image=image_path
                    ))
                    # print(products)
            except Exception as e:
                print(f"Error processing product: {str(e)}")
                continue
        
        return products