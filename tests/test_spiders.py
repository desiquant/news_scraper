import json
import os
import subprocess

import pandas as pd
import pytest


@pytest.fixture(
    params=[
        "businessstandard",
        "businesstoday",
        "economictimes",
        "financialexpress",
        "firstpost",
        "freepressjournal",
        "indianexpress",
        "moneycontrol",
        "ndtvprofit",
        "news18",
        "outlookindia",
        "thehindu",
        "thehindubusinessline",
        "zeenews",
    ]
)
def spider_name(request):
    return request.param


def test_spider_new(spider_name):
    output_file = f"outputs-test/{spider_name}.jl"

    # remove output if exists
    if os.path.isfile(output_file):
        os.remove(output_file)

    settings = {
        "SKIP_OUTPUT_URLS": False,  # Do not skip URLs that have already been processed
        "CLOSESPIDER_ITEMCOUNT": 5,  # Stop after scraping 5 items
        "CONCURRENT_REQUESTS": 5,  # If default concurrent is used, it ignores itemcount limit
        "CLOSESPIDER_TIMEOUT": 30,  # Stop after 30 seconds,
        # Save the outputs to a new temporary file
        "FEEDS": json.dumps({output_file: {"format": "jsonlines", "overwrite": True}}),
        "HTTPCACHE_ENABLED": False,  # Do not cache requests, # ! TEMP: disable cache
        "LOG_FILE": "test-run.log",  # Prevent log from writing to stdout,
    }

    command = ["scrapy", "crawl", spider_name] + [
        f"-s {k}='{v}'" for k, v in settings.items()
    ]

    process = subprocess.run(
        " ".join(command), shell=True, capture_output=True, text=True
    )

    assert (
        process.returncode == 0
    ), f"Scrapy command failed with errors: {process.stderr}"

    # check if spider created output
    if not os.path.isfile(output_file):
        raise FileNotFoundError(output_file)

    df = pd.read_json(output_file, lines=True)

    output_cols = set(df.columns)
    required_cols = {
        "url",
        "title",
        "description",
        "author",
        "date_published",
        "date_modified",
        "article_html",
        "scrapy_scraped_at",
        "scrapy_parsed_at",
    }

    assert output_cols == required_cols
