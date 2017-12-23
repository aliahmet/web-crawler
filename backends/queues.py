import os
import queue


class BaseQueue:
    def __init__(self, crawler_opts):
        self.crawler_opts = crawler_opts

    def push(self, item):
        raise NotImplemented("Queue must have push method")

    def pop(self):
        raise NotImplemented("Queue must have pop method")

    def peek(self):
        raise NotImplemented("Queue must have peek method")

    def is_empty(self):
        raise NotImplemented("Queue must have is_empty method")


class Queue(BaseQueue):
    def __init__(self, crawler_opts):
        super().__init__(crawler_opts)
        self.queue = queue.Queue()

    def push(self, item):
        self.queue.put(item)

    def pop(self):
        return self.queue.get()

    def peek(self):
        return self.queue.queue[0]

    def is_empty(self):
        return self.queue.empty()


class RedisQueue(BaseQueue):
    def __init__(self, crawler_opts, localhost='localhost', port=6379, db=0, queue_name=None, unix_socket_path=None):
        super().__init__(crawler_opts)
        self.init_redis_cli(localhost=localhost, port=port, db=db, unix_socket_path=unix_socket_path)
        self.queue_name = queue_name or os.environ.get("CRAWLER_REDIS_QUEUE_NAME", "") or "CRAWLER_REDIS_QUEUE"

    def get_redis_lib(self):
        try:
            import redis
        except ImportError:
            raise NotImplemented("You need redis-py in order to use RedisQueue backend.")
        return redis

    def get_redis_cli(self, **kwargs):
        redis = self.get_redis_lib()
        self.redis_cli = redis.StrictRedis(**kwargs)

    def init_redis_cli(self, localhost, port, db, unix_socket_path):
        if unix_socket_path:
            self.redis_cli = self.get_redis_cli(unix_socket_path=unix_socket_path)
        else:
            self.redis_cli = self.get_redis_cli(host=localhost, port=port, db=db)

    def push(self, item):
        # Add item in the end of the list
        self.redis_cli.rpush(self.queue_name, item)

    def pop(self):
        # Get item in the start of the list
        top = self.redis_cli.lpop(self.queue_name)

        # Gurantee its type of bytes (handle non)
        top = top or b""

        # convert it to str
        top = str(top)

        return top

    def peek(self):
        # Get item in the start of the list as list
        tops = self.redis_cli.lrange(self.queue_name, 0, 0)

        if len(tops) == 0:
            return None
        top = tops[0]

        # Gurantee its type of bytes (handle non)
        top = top or b""

        # convert it to str
        top = str(top)

        return top

    def is_empty(self):
        # if there is a peek elem,
        # then it is not empty
        return not bool(self.peek())
