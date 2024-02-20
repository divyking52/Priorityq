import queue
import threading
import concurrent.futures

class PriorityMessageQueue:
    def __init__(self):
        self.queue_lock = threading.Lock()
        self.message_queue = queue.PriorityQueue()
        self.receiver_condition = threading.Condition()

    def enq_message(self, message, priority):
        with self.queue_lock:
            self.message_queue.put((priority, message))
            # Notify waiting receiver threads
            with self.receiver_condition:
                self.receiver_condition.notify()

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

def send_message(queue, receiver_condition, message, priority):
    queue.enq_message(message, priority)
    # Notify the receiver thread
    with receiver_condition:
        receiver_condition.notify()

def receive_message(queue):
    while True:
        with queue.receiver_condition:
            while queue.is_empty():
                # Wait for a message to be available
                queue.receiver_condition.wait()
            message = queue.dq_message()
        if message:
            print("Received:", message)

# Example usage
def main():
    pq = PriorityMessageQueue()

    # Set up threads
    receiver_thread = threading.Thread(target=receive_message, args=(pq,), name="Receiver")
    sender_threads = [
        threading.Thread(target=send_message, args=(pq, pq.receiver_condition, f"Hello from sender {i}!", i+1), name=f"Sender {i}")
        for i in range(3)
    ]

    # Start threads
    receiver_thread.start()
    for sender_thread in sender_threads:
        sender_thread.start()

    # Wait for threads to finish
    for sender_thread in sender_threads:
        sender_thread.join()
    receiver_thread.join()

if __name__ == "__main__":
    main()
