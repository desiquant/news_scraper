import glob
import multiprocessing

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from prefect import flow, task
from prefect.tasks import task_input_hash
from scrapy import Spider
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


def run_spider_process(spider):
    process = CrawlerProcess(settings=settings)
    process.crawl(spider)
    process.start()


@task(task_run_name="spider:{spider}")
def run_spider(spider):
    ctx = multiprocessing.get_context("spawn")
    process = ctx.Process(target=run_spider_process, args=(spider,))
    process.start()
    process.join()


# @flow
# def run_spiders_A():
#     run_spider("thehindu")


@flow
def run_spiders():
    spiders = [
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

    return run_spider.map(spiders)


@flow(flow_run_name="run_spiders")
def new_scraper():
    run_spiders()
    convert_to_parquet()


@task(log_prints=True)
def convert_to_parquet():
    file_paths = glob.glob("data/outputs/*.jl")
    output_file = "data/dump.parquet"

    writer = None
    total_files = len(file_paths)

    print(f"Found {len(file_paths)} files to process.")

    for file_index, file_path in enumerate(file_paths, 1):
        reader = pd.read_json(file_path, lines=True, chunksize=20000)

        for chunk in reader:
            table = pa.Table.from_pandas(chunk)

            if writer is None:
                writer = pq.ParquetWriter(output_file, table.schema)

            writer.write_table(table)

        print(f"Processed file {file_index}/{total_files}: {file_path}")

    if writer:
        writer.close()
        print(f"All data written to {output_file}")
    else:
        print("No data was processed")

    print("All files processed.")

    return output_file


if __name__ == "__main__":
    # run_spiders_A.serve(name="daily_news")
    new_scraper()
