 
import time
import random
import queue

message_queue = queue.Queue(maxsize=1)
processed_event = threading.Event()


def producer():
    """Генератор: створює повідомлення і чекає на обробку"""
    for message_id in range(1, 6):
        time.sleep(random.uniform(0.5, 1.5))
        msg = f"Повідомлення №{message_id}"
        message_queue.put(msg)
        print(f"[Генератор] Створив: {msg}")

        processed_event.wait()
        processed_event.clear()
        print(f"[Генератор] Отримав підтвердження, готую наступне...\n")

    message_queue.put(None)


def consumer():
    """Обробник: отримує повідомлення, виводить і дає сигнал генератору"""
    while True:
        msg = message_queue.get()
        if msg is None:
            break

        time.sleep(2)
        print(f"--- [Обробник] Обробив: {msg}")

        processed_event.set()
        message_queue.task_done()


if __name__ == "__main__":
    p_thread = threading.Thread(target=producer)
    c_thread = threading.Thread(target=consumer)

    p_thread.start()
    c_thread.start()

    p_thread.join()
    c_thread.join()
    print("Програма завершена.")