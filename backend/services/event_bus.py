from queue import Queue


class EventBus:
    _STOP = object()

    def __init__(self):
        self.queue = Queue()

    def emit(self, event):
        self.queue.put(event)

    def stop(self):
        self.queue.put(self._STOP)

    def next_event(self):
        event = self.queue.get()
        if event is self._STOP:
            return None
        return event
