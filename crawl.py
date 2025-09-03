from urllib.parse import urlparse
from get_html import get_html
from get_from_html import get_urls_from_html
from get_from_html import extract_page_data
from normalize_url import normalize_url
from concurrency import AsyncCrawler


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url == None:
        current_url = base_url
    if page_data == None:
        page_data = {}
    
    base_host = urlparse(base_url).netloc
    current_host = urlparse(current_url).netloc
    if current_host != base_host:
        return page_data

    norm_url = normalize_url(current_url)
    if norm_url in page_data:
        return page_data
    
    try:
        current_html = get_html(current_url)
    except RuntimeError as e:
         print(f"Skipping {current_url}: {e}")
         return page_data


    print(f'currently crawling {current_url}')
    page_data[norm_url] = extract_page_data(current_html, current_url)
    urls = get_urls_from_html(current_html, base_url)
    for page in urls:
        crawl_page(base_url, page, page_data)
    return page_data

async def crawl_site_async(url, max_conc, max_pages):
    async with AsyncCrawler(url, max_conc, max_pages) as async_crawler:
        await async_crawler.crawl()
        return async_crawler.page_data