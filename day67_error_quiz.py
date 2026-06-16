# Day 67 - Error Finding Quiz

import threading
import time

counter = 0
lock = threading.Lock()

def increment(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1


def worker(name, delay):
    print(f"Worker {name} starting")
    time.sleep(delay)
    print(f"Worker {name} done")


# Bug 1 - thread started incorrectly
t1 = threading.Thread(target=worker, args=("A", 0.1))
t1.start
t1.join()    # Bug 1 - start not called (missing ())

# Bug 2 - daemon thread
t2 = threading.Thread(target=worker, args=("B", 2))
t2.daemon = True
t2.start()
# Bug 2 - no join(), daemon thread may not complete before main exits

# Event
stop_event = threading.Event()

def monitor(event):
    while not event.is_set():
        print("  Monitoring...")
        time.sleep(0.1)
    print("  Monitor stopped.")

t3 = threading.Thread(target=monitor, args=(stop_event,))
t3.start()
time.sleep(0.3)
stop_event.set
# Bug 3 - stop_event.set missing () — event never set, thread never stops

t3.join(timeout=1)