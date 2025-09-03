from urllib.parse import urlparse

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = parsed_url.hostname + parsed_url.path
    return normalized_url.rstrip("/")