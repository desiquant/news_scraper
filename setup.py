from setuptools import setup, find_packages

setup(
    name="dq_news",
    description="Scrapes indian market news from popular online indian ews outlets",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scrapy",
        "pandas",
        "netifaces",
        "fake-useragent",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/desiquant/dq_news",
    python_requires=">=3.6",
)
