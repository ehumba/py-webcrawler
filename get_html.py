import requests

def get_html(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        if "text/html" not in res.headers["content-type"]:
            raise Exception("invalid content type")
        return res.text
    except Exception as e:
        raise RuntimeError(f"failed to fetch {url}: {e}")
