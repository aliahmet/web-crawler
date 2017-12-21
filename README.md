## Simple Web Crawler

A simple web crawler to create sitemap of a given website.


#### USAGE (bash):
```
main.py -u http://flask.pocoo.org/docs/0.12/index.html
            # Generate sitemap of http://flask.pocoo.org/docs/0.12/ directory
main.py -u http://flask.pocoo.org/docs/0.12/index.html -b http://flask.pocoo.org/docs/
            # Generate sitemap of http://flask.pocoo.org/docs/ directory starting from /docs/0.12/index.html
main.py -u ... -vvv
            # set logging to very verbose
main.py -u ... -o sitemap.xml
            # Write generated sitemap to sitemap.xml file
```
#### USAGE (python):
```python

crawler = WebCrawler()
crawler.crawl(url)
result = crawler.dump()

# You can use your own backends
class SuperFastCsvWebCrawler(WebCrawler):
    # Custom Backend Classes
    storage_class = SuperFastUrlStorage
    http_client_class = SuperFastHttpClient
    encoder_class = CSVEncoder
    
    def get_to_visit_queue():
        # Custom initilize
        return RedisQueue(self.opts, host="127.0.0.1", port=6379, db=2)


```
#### Design Notes

+ All links are stored and visited with absolute urls in order to prevent duplicates

+ Helper classes are pluggable, for instance, 
you can put your own csv encoder.

+ Default UrlStorage is a dict so that registering, finding, 
unregistered are all in O(1).   

+ I preferred BFS over DFS because 1. page order is more natural, 2. 
recursive graph uses a lot of memory, 3. Supports multiple workers.

+ I joined xml tag strings to create final xml instead of using a real 
encoder to keep it simple. (as mentinoed above it is very simple to use
 a more broad encoder)

+ This project first crawls everything then writes into file, if we want 
to crawl very big pages we may think of possible optimizations:
  + Write to file as it crawls to prevent memory leak.
  + Create multiple sub sitemaps for different sub directories to run several workers.
  + An external queue like redis or RabbitMQ to coordinate multiple workers.

####  Test:

There is a unit test coverege:

```bash
pytest test.py
```
