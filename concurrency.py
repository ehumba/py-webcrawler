import asyncio
import aiohttp
from get_from_html import extract_page_data
from get_from_html import get_urls_from_html
from normalize_url import normalize_url
from urllib.parse import urlparse

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_host = urlparse(self.base_url).netloc
        self.page_data = {}
        self.max_pages = max_pages
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
     self.session = aiohttp.ClientSession()
     return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
       await self.session.close()


    async def add_page_visit(self, normalized_url):
       if self.should_stop == True:
          return False
       
       async with self.lock:
           if len(self.page_data) >= self.max_pages:
              self.should_stop = True
              print("Reached maximum number of pages to crawl.")
              for task in self.all_tasks:
                 task.cancel()
              return False
           
           if normalized_url in self.page_data:
             return False
           self.page_data[normalized_url] = None
           return True
       

    async def get_html(self, url):
       async with self.session.get(url) as resp:
        if resp.status >= 400:
         raise RuntimeError(f"Bad response {resp.status} for {url}")
        if not resp.content_type.startswith("text/html"):
         raise RuntimeError(f"Invalid content type {resp.content_type} at {url}")

        return await resp.text()
       

    async def crawl_page(self, current_url=None):
       if self.should_stop == True:
          return
       if current_url == None:
          current_url = self.base_url
        
       normalized_url = normalize_url(current_url)
       visited = await self.add_page_visit(normalized_url)
       if visited == False:
          return
       
       current_host = urlparse(current_url).netloc
       if current_host != self.base_host:
          return 
       
       async with self.semaphore:
          try:
            current_html = await self.get_html(current_url)
          except RuntimeError as e:
             print(f"Skipping {current_url}: {e}")
             return
             
          print(f"currently crawling: {current_url}")
          current_data = extract_page_data(current_html, current_url)
          async with self.lock:
             self.page_data[normalized_url] = current_data

          urls = get_urls_from_html(current_html, self.base_url)
          tasks = []
          for page in urls:
                task = asyncio.create_task(self.crawl_page(page))
                self.all_tasks.add(task)
                task.add_done_callback(self.all_tasks.discard)
                tasks.append(task)
          if tasks:
             await asyncio.gather(*tasks, return_exceptions=True) 

   
    async def crawl(self):
       await self.crawl_page(self.base_url)
       return self.page_data
       