from setuptools import find_packages, setup

setup(
    name="news_scraper",
    description="Scrapes indian market news from popular online indian ews outlets",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scrapy",
        "pandas",
        "netifaces",
        "fake-useragent",
    ],
    test_requires=[
        "pytest",
        "syrupy",
    ],
    url="https://github.com/desiquant/news_scraper",
    python_requires=">=3.10",
)
