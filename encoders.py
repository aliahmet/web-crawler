class SitemapGenerator:
    def __init__(self, data):
        self.data = data

    def dumps(self, indent=4):
        """

        """
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for page, props in self.data.items():
            lines += [(" " * indent) + "<url>"]
            lines += [(" " * indent * 2) + "<{key}>{val}</{key}>".format(key=key, val=val) for key, val in
                      props.items()]
            lines += [(" " * indent) + "</url>"]
        lines += [
            "</urlset>",
            ""  # empty line at the eof
        ]
        return ("\n" if indent else "").join(lines)
