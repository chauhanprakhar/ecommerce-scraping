# Web Scraping Tool

A FastAPI-based web scraping tool designed to efficiently scrape product information from e-commerce websites. The tool features configurable settings, caching mechanisms, and extensible storage options.

## Features

- 🚀 Asynchronous web scraping
- 🔒 API key authentication
- 💾 Configurable storage strategies
- 📦 Redis-based caching system
- 🔄 Automatic retry mechanism
- 🌐 Proxy support
- 📧 Extensible notification system

## Prerequisites

- Python 3.8+
- Redis server
- Virtual environment (recommended)

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd scraping-tool
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:
```env
AUTH_TOKEN=your-secret-token
REDIS_URL=redis://localhost:6379
DEFAULT_TARGET_URL=https://example-shop.com
RETRY_ATTEMPTS=3
RETRY_DELAY=5
```

## Project Structure
```
app/
├── __init__.py
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   └── schema.py
├── scraper/
│   ├── __init__.py
│   └── scraper.py
├── storage/
│   ├── __init__.py
│   └── json_storage.py
├── notifications/
│   ├── __init__.py
│   └── console.py
└── cache/
    ├── __init__.py
    └── redis_cache.py
```

## Usage

1. Start the application:
```bash
uvicorn app.main:app --reload
```
PS: Please don't forget to run Redis first

2. Make a scraping request:
```bash
curl -X POST "http://localhost:8000/scrape/" \
-H "X-API-Key: your-secret-token" \
-H "Content-Type: application/json" \
-d '{
  "page_limit": 5,
  "proxy": "http://proxy.example.com:8080",
  "target_url": "https://example-shop.com"
}'
```

## API Documentation

### POST /scrape/
Scrapes product information from the specified website.

**Request Body:**
```json
{
  "page_limit": 5,          // Optional: Limit number of pages to scrape
  "proxy": "http://...",    // Optional: Proxy server URL
  "target_url": "https://..." // Optional: Target website URL
}
```

**Response:**
```json
[
  {
    "product_title": "Example Product",
    "product_price": 299.99,
    "path_to_image": "images/example-product.jpg"
  }
]
```
Response will also be saved as JSON in product.json file which will be created when  you hit the /scrape endpoint
![image](https://github.com/user-attachments/assets/d98012f5-dcbd-466c-8df4-94cbbd8953d0)

Images will be saved to a folder named images which will also be created when you hit the /scrape endpoint
![image](https://github.com/user-attachments/assets/8bac9603-f1d5-47e1-a846-c61bb0cf95e7)




## Error Handling

The application includes comprehensive error handling:
- Authentication errors (403)
- Invalid input validation (422)
- Automatic retry for failed requests
- Rate limiting protection

