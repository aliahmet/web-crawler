import argparse
import logging
import sys
from urllib.parse import urljoin

import lxml.html

from backends.encoders import SitemapEncoder
from backends.http_clients import HttpClient
from backends.queues import Queue
from backends.sets import Set
from backends.storage import UrlStorage

logger = logging.getLogger(__name__)


class WebCrawler():
    storage_class = UrlStorage
    http_client_class = HttpClient
    encoder_class = SitemapEncoder
    to_visit_queue_class = Queue
    visited_set_class = Set


    def __init__(self, exclude_broken_links=False, keep_alive=False):
        self.keep_alive = keep_alive
        self.exclude_broken_links = exclude_broken_links

        self.crawled_pages = self.get_crawled_pages_storage()
        self.http_client = self.get_http_client()
        self.to_visit = self.get_to_visit_queue()
        self.visited_set = self.get_visited_set()

    def get_visited_set(self):
        return self.visited_set_class()

    def get_to_visit_queue(self):
        return self.to_visit_queue_class()

    def get_http_client(self):
        return self.http_client_class(self.keep_alive)

    def get_crawled_pages_storage(self):
        return self.storage_class()



    def normalize_url(self, base_url, url):
        """
        Convert url to absolute url and remove anchors and get parameters
        """
        url = url.split("#")[0]  # clear anchors
        url = url.split("?")[0]  # clear get parameters (?)
        return urljoin(base_url, url)

    def parse_links(self, base_url, content):
        """
        Parse href's in a page and make them absolute links
        """
        elem = lxml.html.fromstring(content)
        raw_urls = elem.xpath('//a/@href')
        return [self.normalize_url(base_url=base_url, url=url) for url in raw_urls]

    def register_url(self, url, response):
        self.crawled_pages.register_url(url, {
            "loc": url,
            "lastmod": self.http_client.get_last_modified(response)
        })

    def unregister_url(self, url):
        self.crawled_pages.unregister_url(url)

    def is_external(self, base_url, url):
        if not url.startswith(base_url):
            logger.info("Ignoring External Link: %s" % url)
            return True
        else:
            return False

    def crawl(self, start_url, base_url=None):
        base_url = base_url or urljoin(start_url, ".")
        # Limit sub pages to parent of starting page if not specified

        self.to_visit.push(start_url)

        while not self.to_visit.is_empty():
            current_page = self.to_visit.pop()
            logger.info("Visiting: %s" % current_page)
            response = self.http_client.get(current_page)

            self.register_url(current_page, response)
            current_page = response.url  # handles 301, 302

            if self.is_external(base_url, url=current_page):
                continue

            if not self.http_client.can_crawl(response):
                logger.info("Broken Link: %s" % current_page)
                if not self.exclude_broken_links:
                    self.unregister_url(current_page)
                continue

            child_links = self.parse_links(current_page, response.content)
            for child_link in child_links:
                if child_link not in self.visited_set and not self.is_external(base_url, child_link):
                    logger.info("%s -> %s" % (current_page, child_link))
                    self.to_visit.push(child_link)
                    self.visited_set.add(child_link)
        return self.crawled_pages

    def dump(self, indent=4):
        return self.encoder_class(self.crawled_pages).dumps(indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url',
                        help='Url to crawl',
                        required=True)
    parser.add_argument('-b', '--base_url',
                        help='Limit pages to a base url',
                        required=False,
                        default=None
                        )
    parser.add_argument('-k', '--keep_alive',
                        help='Keep client alive while crawling',
                        action="store_true",
                        )
    parser.add_argument('-e', '--exclude_broken_links',
                        help='Exclude broken links from sitemap',
                        action="store_true",
                        )

    parser.add_argument('-v', '--verbose',
                        dest="loglevel",
                        action='count',
                        help="Logging level -v/-vv/-vvv",
                        default=0
                        )

    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="Output file  (default: stdout)"
                        )
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]

    args = parser.parse_args()
    logging.basicConfig(level=levels[args.loglevel])
    crawler = WebCrawler(
        keep_alive=args.keep_alive,
        exclude_broken_links=args.exclude_broken_links

    )
    crawler.crawl(
        start_url=args.url,
        base_url=args.base_url
    )
    result = crawler.dump()
    with args.output as output:
        output.write(result)
