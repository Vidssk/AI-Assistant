from queue import Queue

# class EventBus:
#     def __init__(self):
#         self.queue = Queue()

#     def emit(self, event):
#         self.queue.put(event)

#     def next_event(self):
#         return self.queue.get()
class EventBus:
    def __init__(self):
        self.queue = Queue()

    def emit(self, event):
        self.queue.put(event)

    def next_event(self):
        return self.queue.get()  # blocking is fine HERE