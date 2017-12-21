import requests
from datetime import datetime


class HttpClient:
    """
    Wrapper for requests for web communication
    """
    HTTP_RESPONSE_OK = 200

    def __init__(self, crawler_opts):
        self.crawler_opts = crawler_opts
        if crawler_opts.keep_alive:
            self.handler = requests.session()
        else:
            self.handler = requests

    def get(self, url):
        return requests.get(url)

    def is_html(self, response):
        return "text/html" in response.headers.get("Content-Type", "text/plain").split(";")
        # Header may contain encoding. ex: `Content-Type: text/html; utf-8`

    def get_last_modified(self, response):
        return response.headers.get("Last-Modified", None) or \
               response.headers.get("Date", None) or \
               datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def can_crawl(self, response):
        return self.is_html(response) and \
               self.get_last_modified(response)
