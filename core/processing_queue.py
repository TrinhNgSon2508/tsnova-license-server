from queue import Queue


class ProcessingQueue:

    def __init__(self):

        self.queue = Queue()

    def add_task(self, file_path):

        self.queue.put(file_path)

    def get_task(self):

        return self.queue.get()

    def task_done(self):

        self.queue.task_done()

    def clear(self):

        while not self.queue.empty():

            self.queue.get()

            self.queue.task_done()


processing_queue = ProcessingQueue()