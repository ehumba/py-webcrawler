import sys
from crawl import crawl_site_async
import asyncio
from csv_report import write_csv_report


async def main_async():
    if len(sys.argv) != 4:
        print("Three arguments required: URL, maximum concurrency, maximum pages")
        sys.exit(1)

    url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])

    print(f"Starting crawl of: {url}")

    crawl_result = await crawl_site_async(url, max_concurrency, max_pages)
    write_csv_report(crawl_result)



asyncio.run(main_async())
