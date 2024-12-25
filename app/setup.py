# setup.py
from setuptools import setup, find_packages

setup(
    name="scraping_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "httpx",
        "beautifulsoup4",
        "redis",
        "pydantic"
    ],
)