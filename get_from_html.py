from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1')
    if h1 == None:
        return ""
    return soup.h1.get_text()


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('main') == None:
        first_para = soup.find('p')
        if first_para == None:
            return ""
        return soup.p.get_text()
    first_para = soup.main.find('p')
    if first_para == None:
        return ""
    return soup.main.p.get_text()


def get_urls_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
        return urls
    except Exception as e:
        return [], e
    

def get_images_from_html(html, base_url):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for link in soup.find_all('img', src=True):
            src = link.get('src')
            absolute_url = urljoin(base_url, src)
            urls.append(absolute_url)
        return urls
    except Exception as e:
        return [], e
    

def extract_page_data(html, page_url):
    page_data = {}
    page_data['url'] = page_url
    page_data['h1'] = get_h1_from_html(html)
    page_data['first_paragraph'] = get_first_paragraph_from_html(html)
    page_data['outgoing_links'] = get_urls_from_html(html, page_url)
    page_data['image_urls'] = get_images_from_html(html, page_url)
    return page_data