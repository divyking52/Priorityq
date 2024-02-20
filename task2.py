import queue
import concurrent.futures

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

def message_consumer(queue):
    while True:
        message = queue.dq_message()
        if message:
            print("Consumed:", message)
        else:
            break

# Example usage
def main():
    pq = PriorityMessageQueue()
    message_data = [("Message 1", 3), ("Message 2", 1), ("Message 3", 2), ("Message 4", 5), ("Message 5", 4)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for message, priority in message_data:
            executor.submit(pq.enq_message, message, priority)

        executor.submit(message_consumer, pq)

if __name__ == "__main__":
    main()
