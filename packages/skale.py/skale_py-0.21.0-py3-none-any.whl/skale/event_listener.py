import logging
from threading import Thread
from time import sleep

logger = logging.getLogger(__name__)


class EventListener():
    def __init__(self, event, handler, poll_interval, opts={}):
        logger.info(f'adding listener: {event.__name__}, handler: {handler.__name__}, poll_interval: {poll_interval}')
        self.event = event
        self.filter = event.createFilter(fromBlock=1)
        self.poll_interval = poll_interval
        self.handler = handler

    def loop(self):
        while True:
            try:
                for event in self.filter.get_new_entries():
                    self.handler(event)
                sleep(self.poll_interval)
            except:
                logger.exception(
                    f'Error was occurred during the event polling: {self.event.__name__}, handler: {self.handler.__name__}. See full stacktrace below.')
                # todo: handle

    def run(self):
        self.worker = Thread(target=self.loop)
        self.worker.start()

    def stop(self):
        self.worker.join()
