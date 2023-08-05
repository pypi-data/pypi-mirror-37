from queue import Queue


class NotifyHandler:
    def __init__(self, maxsize=0):
        self.queue = Queue()

    def emit(self, record):
        self.queue.put_nowait(record)
