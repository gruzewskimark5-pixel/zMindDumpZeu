import logging
import queue
import threading
import time
import signal
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.queue = queue.Queue()
        self.running = False
        self.worker_thread = None

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(f"Subscribed to {event_type}")

    def publish(self, event_type, data):
        self.queue.put((event_type, data))
        logger.info(f"Published {event_type}")

    def start(self):
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        logger.info("EventBus started")

    def stop(self):
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
        logger.info("EventBus stopped")

    def _process_queue(self):
        while self.running:
            try:
                event_type, data = self.queue.get(timeout=1)
                if event_type in self.subscribers:
                    for callback in self.subscribers[event_type]:
                        try:
                            callback(data)
                        except Exception as e:
                            logger.error(f"Error in subscriber for {event_type}: {e}")
            except queue.Empty:
                continue

def signal_handler(sig, frame):
    logger.info('Stopping EventBus...')
    if 'bus' in globals():
        bus.stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    bus = EventBus()
    bus.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bus.stop()
