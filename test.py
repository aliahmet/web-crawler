from collections import OrderedDict
from unittest import TestCase


class TestEncoder(TestCase):
    def test_check_simple_encoder(self):
        from encoders import SitemapGenerator
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/", {
            "loc": "http://example.com/"
        })
        dumped_result = SitemapGenerator(storage).dumps(indent=0)
        expected = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' \
                   '<url>' \
                   '<loc>http://example.com/</loc>' \
                   '</url>' \
                   '</urlset>'

        self.assertEqual(expected, dumped_result)

    def test_check_location_override(self):
        from encoders import SitemapGenerator
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/", {
            "loc": "http://example.com/index.html"
        })
        dumped_result = SitemapGenerator(storage).dumps(indent=0)
        expected = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' \
                   '<url>' \
                   '<loc>http://example.com/index.html</loc>' \
                   '</url>' \
                   '</urlset>'

        self.assertEqual(expected, dumped_result)

    def test_check_no_location(self):
        from encoders import SitemapGenerator
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/")
        dumped_result = SitemapGenerator(storage).dumps(indent=0)
        expected = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' \
                   '<url>' \
                   '<loc>http://example.com/</loc>' \
                   '</url>' \
                   '</urlset>'

        self.assertEqual(expected, dumped_result)

    def test_check_encode_with_props(self):
        from encoders import SitemapGenerator
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/", OrderedDict(
            (
                ("priority", 1),
                ("loc", "http://example.com/"),
            )
        ))
        dumped_result = SitemapGenerator(storage).dumps(indent=0)
        expected = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' \
                   '<url>' \
                   '<priority>1</priority>' \
                   '<loc>http://example.com/</loc>' \
                   '</url>' \
                   '</urlset>'
        self.assertEqual(expected, dumped_result)


class TestStorage(TestCase):
    def test_check_storage_add(self):
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/")
        storage.register_url("http://example.com/aa.html")
        storage.register_url("http://example.com/bb.html")
        self.assertEqual(3, len(list(storage.urls.values())))

    def test_check_storage_remove(self):
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/")
        storage.register_url("http://example.com/aa.html")
        storage.unregister_url("http://example.com/aa.html")
        self.assertEqual(1, len(list(storage.urls.values())))

    def test_check_storage_remove_nonexisting(self):
        from storage import UrlStorage
        storage = UrlStorage()
        storage.register_url("http://example.com/")
        storage.register_url("http://example.com/aa.html")
        try:
            storage.unregister_url("http://example.com/bb.html")
        except KeyError:
            pass
        else:
            assert "No exception raised"

    def test_iter_all_links(self):
        from storage import UrlStorage
        storage = UrlStorage()
        links = [
            "http://example.com/",
            "http://example.com/aa.html",
            "http://example.com/bb.html",
            "http://example.com/cc/dd.html",
        ]
        for link in links:
            storage.register_url(link)

        for link in storage:
            links.pop(links.index(link))
        self.assertEqual([], links)


class TestParser(TestCase):
    def test_parse_links(self):
        from main import WebCrawler
        base_url = "http://example.com/"
        html = '<html>' \
               '<a href="http://example.com/aa.html"></a>' \
               '</html>'
        crawler = WebCrawler()
        links = crawler.parse_links(base_url, html)
        self.assertEqual(links, ['http://example.com/aa.html'])

    def test_parse_relative_links(self):
        from main import WebCrawler
        base_url = "http://example.com/"
        html = '<html>' \
               '<a href="/aa.html"></a>' \
               '</html>'
        crawler = WebCrawler()
        links = crawler.parse_links(base_url, html)
        self.assertEqual(links, ['http://example.com/aa.html'])

    def test_parse_inner_root_links(self):
        from main import WebCrawler
        base_url = "http://example.com/aa/bb/vv"
        html = '<html>' \
               '<a href="/aa.html"></a>' \
               '</html>'
        crawler = WebCrawler()
        links = crawler.parse_links(base_url, html)
        self.assertEqual(links, ['http://example.com/aa.html'])

    def test_parse_inner_parent_links(self):
        from main import WebCrawler
        base_url = "http://example.com/aa/bb/"
        html = '<html>' \
               '<a href="../cc.html"></a>' \
               '</html>'
        crawler = WebCrawler()
        links = crawler.parse_links(base_url, html)
        self.assertEqual(links, ['http://example.com/aa/cc.html'])

    def test_parse_external_links(self):
        from main import WebCrawler
        base_url = "http://example.com/aa/bb/"
        html = '<html>' \
               '<a href="http://google.com/cc.html"></a>' \
               '</html>'
        crawler = WebCrawler()
        links = crawler.parse_links(base_url, html)
        self.assertEqual(links, ["http://google.com/cc.html"])
