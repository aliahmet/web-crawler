class BaseQueue:
    def push(self, item):
        raise NotImplemented("Queue must have push method")

    def pop(self):
        raise NotImplemented("Queue must have pop method")

    def peek(self):
        raise NotImplemented("Queue must have peek method")

    def is_empty(self):
        raise NotImplemented("Queue must have is_empty method")


class Queue(BaseQueue):
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop()

    def peek(self):
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0
