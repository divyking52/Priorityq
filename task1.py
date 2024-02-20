import queue
import threading

class PriorityMessageQueue:
    def __init__(self):
        self.queue_lock = threading.Lock()
        self.message_queue = queue.PriorityQueue()

    def enq_message(self, message, priority):
        with self.queue_lock:
            self.message_queue.put((priority, message))

    def dq_message(self):
        with self.queue_lock:
            if not self.message_queue.empty():
                return self.message_queue.get()[1]
            else:
                return None

    def peek_message(self):
        with self.queue_lock:
            if not self.message_queue.empty():
                return self.message_queue.queue[0][1]
            else:
                return None

    def is_empty(self):
        with self.queue_lock:
            return self.message_queue.empty()

# Example usage
def producer(queue):
    for i in range(10):
        queue.enq_message(f"Message {i}", priority=i)

def consumer(queue):
    while not queue.is_empty():
        message = queue.dq_message()
        if message:
            print("Consumed:", message)

if __name__ == "__main__":
    pq = PriorityMessageQueue()

    producer_thread = threading.Thread(target=producer, args=(pq,))
    consumer_thread = threading.Thread(target=consumer, args=(pq,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
