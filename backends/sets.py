class BaseSet:

    def __init__(self, crawler_opts):
        self.crawler_opts = crawler_opts

    def __contains__(self, item):
        raise NotImplemented("Set must have __contains__ method")

    def add(self, element):
        raise NotImplemented("Set must have add method")

    def remove(self, element):
        raise NotImplemented("Set must have remove method")


class Set(BaseSet):
    def __init__(self, crawler_opts):
        super().__init__(crawler_opts)
        self.set = set()

    def __contains__(self, item):
        return item in self.set

    def add(self, element):
        self.set.add(element)

    def remove(self, element):
        self.set.remove(element)
