from collections import OrderedDict


class BaseUrlStorage:
    def __init__(self, crawler_opts):
        self.crawler_opts = crawler_opts

    def register_url(self, url, props=None):
        raise NotImplemented("UrlStorage must have register_url method")

    def unregister_url(self, url):
        raise NotImplemented("UrlStorage must have unregister_url method")

    def __iter__(self):
        raise NotImplemented("UrlStorage must have __iter__ method")

    def items(self):
        raise NotImplemented("UrlStorage must have __iter__ method")


class UrlStorage(BaseUrlStorage):
    """
    Wrapper for a dict object to store visited urls along
     with other props
    """

    def __init__(self, crawler_opts):
        super().__init__(crawler_opts)
        self.urls = OrderedDict()

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
