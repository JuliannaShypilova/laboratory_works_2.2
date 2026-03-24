import threading
import time
import random
from collections import deque


class PriorityDeque:
    def __init__(self):
        self._container = deque()
        self._lock = threading.Lock()

    def add_message(self, priority, data):
        with self._lock:
            if priority == 1:
                self._container.appendleft((priority, data))
                print(f"[Генератор] Надіслав ПРІОРИТЕТНУ: {data}")
            else:
                self._container.append((priority, data))
                print(f"[Генератор] Надіслав звичайну: {data}")

    def get_message(self):
        with self._lock:
            if self._container:
                return self._container.popleft()
            return None


my_queue = PriorityDeque()


def producer():
    for i in range(1, 11):
        priority = 1 if i in [3, 7] else 2
        my_queue.add_message(priority, f"Задача №{i}")
        time.sleep(0.1)

    my_queue.add_message(3, None)


def consumer():
    print("--- [Обробник] Починає роботу через 2 секунди (чекає наповнення черги)... ---")
    time.sleep(2)

    while True:
        item = my_queue.get_message()
        if item is None:
            time.sleep(0.2)
            continue

        priority, msg = item
        if msg is None: break

        print(f"--- [Обробник] ОБРОБЛЯЄ: {msg} (Пріоритет: {priority})")
        time.sleep(1)
    print("--- [Обробник] Роботу завершено. ---")


if __name__ == "__main__":
    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start()
    c.start()
    p.join()
    c.join()