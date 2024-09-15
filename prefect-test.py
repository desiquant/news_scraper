# PROBLEM: The concurrent parallel execution of multiple scrapy spiders is being ignored because it works the flow runs from the script like prefect-test.py but doesn't stop after scraping when prefect executes the flow. This has something to do with multiprocessing context and I was unable to fix it. Moreover, the ETL part of the news_scraper is being moved to another python module and hence this file will be removed soon.

from glob import glob

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

SPIDER_OUTPUT_PATHS = glob("data/outputs/*.jl")
DATA_FILEPATH = "data/news.parquet"
S3_FILE_KEY = "data/news.parquet"


def run_spider_process(spider):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    settings = get_project_settings()
    settings.update(
        {
            "SKIP_OUTPUT_URLS": False,  # Do not skip URLs that have already been processed
            "CLOSESPIDER_ITEMCOUNT": 10,  # Stop after scraping 5 items
            "CONCURRENT_REQUESTS": 5,  # If default concurrent is used, it ignores itemcount limit
            "CLOSESPIDER_TIMEOUT": 30,  # Stop after 30 seconds,
            # Save the outputs to a new temporary file
            "HTTPCACHE_ENABLED": True,  # Do not cache requests, # ! TEMP: disable cache
            "LOG_FILE": "test-run.log",  # Prevent log from writing to stdout,
        }
    )

    process = CrawlerProcess(settings=settings)
    process.crawl(spider)
    process.start()


@task(task_run_name="spider:{spider}")
def run_spider(spider):
    import multiprocessing

    # ctx = multiprocessing.get_context("spawn")
    ctx = multiprocessing
    process = ctx.Process(target=run_spider_process, args=(spider,))
    process.start()
    process.join()


# @flow
# def run_spiders_A():
#     run_spider("thehindu")


@flow(task_runner=ConcurrentTaskRunner())
def run_spiders():
    spiders = [
        "businessstandard",
        "businesstoday",
        # "economictimes",
        # "financialexpress",
        # "firstpost",
        # "freepressjournal",
        # "indianexpress",
        # "moneycontrol",
        # "ndtvprofit",
        # "news18",
        # "outlookindia",
        # "thehindu",
        # "thehindubusinessline",
        # "zeenews",
    ]

    return run_spider.map(spiders)


@task()
def convert_to_parquet():
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    writer = None

    for i, file_path in enumerate(SPIDER_OUTPUT_PATHS, 1):
        reader = pd.read_json(file_path, lines=True, chunksize=20000)

        for chunk in reader:
            table = pa.Table.from_pandas(chunk)

            if writer is None:
                writer = pq.ParquetWriter(DATA_FILEPATH, table.schema)

            writer.write_table(table)

    if writer:
        writer.close()

    return DATA_FILEPATH


@task
def upload_to_s3():
    import os

    import boto3
    from dotenv import load_dotenv

    load_dotenv(override=True)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
    )

    s3.upload_file(DATA_FILEPATH, os.getenv("AWS_S3_BUCKET"), S3_FILE_KEY)


@flow(flow_run_name="run_spiders")
def new_scraper():
    run_spiders()
    # convert_to_parquet()
    # upload_to_s3()


if __name__ == "__main__":
    # new_scraper.serve(name="daily_news")

    # works with ctx = multiprocessing.get_context("spawn")
    # run_spiders()

    # doesnt work
    run_spiders.serve(name="daily_news")

    # new_scraper()
    # upload_to_s3()
