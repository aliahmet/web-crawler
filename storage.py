class UrlStorage():
    def __init__(self):
        self.urls = {}

    def register_url(self, url, props=None):
        props = props or {}
        props.setdefault("loc", url)
        self.urls[url] = props


    def unregister_url(self, url):
        self.urls.pop(url)

    def __iter__(self):
        return iter(self.urls)

    def items(self):
        return self.urls.items()
