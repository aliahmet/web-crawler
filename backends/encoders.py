class BaseEncoder:
    def __init__(self, crawler_opts):
        self.crawler_opts = crawler_opts

    def dumps(self, data, indent=4):
        raise NotImplemented("Encoder must have dumps method")


class SitemapEncoder(BaseEncoder):
    """
    Turn storage in to sitemap xml string
    """

    def dumps(self, data, indent=4):
        """
        Returns encoded xml string
        """
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for page, props in data.items():
            lines += [(" " * indent) + "<url>"]
            lines += [(" " * indent * 2) + "<{key}>{val}</{key}>".format(key=key, val=val) for key, val in
                      props.items()]
            lines += [(" " * indent) + "</url>"]
        lines += [
            "</urlset>",
            ""  # empty line at the eof
        ]
        return ("\n" if indent else "").join(lines)
