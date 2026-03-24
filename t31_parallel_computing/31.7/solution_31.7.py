import threading
import time
import random
from queue import Queue

N = 10    # Загальна кількість кас
M = 3     # Початкова кількість працюючих касирів
K = 5     # Початкова кількість покупців у чергах
T1 = 2    # Макс. інтервал приходу покупця
T2 = 3    # Макс. час обслуговування
T3 = 10   # Інтервал, через який касир йде на перерву
T4 = 2    # Час перерви
L_MAX = 5  # Максимальна довжина черги до одного касира


class Cashier(threading.Thread):
    def __init__(self, id, is_reserve=False):
        super().__init__()
        self.id = id
        self.queue = Queue()
        self.is_active = True
        self.is_reserve = is_reserve
        self.daemon = True

    def run(self):
        while self.is_active:
            if not self.queue.empty():
                customer = self.queue.get()
                print(f"[Каса {self.id}] Обслуговує покупця {customer}...")
                time.sleep(random.uniform(1, T2))
                print(f"[Каса {self.id}] Завершила обслуговування {customer}.")
                self.queue.task_done()

                if not self.is_reserve and random.random() < 0.1:
                    print(f"!!! [Каса {self.id}] Йде на перерву на {T4} сек.")
                    time.sleep(T4)
            else:
                time.sleep(0.5)


def supervisor():
    """Потік адміністрації: стежить за довжиною черг та додає резервні каси"""
    active_cashiers = [Cashier(i) for i in range(1, M + 1)]
    reserve_cashiers = []

    for c in active_cashiers:
        for j in range(K):
            c.queue.put(f"{c.id}_{j}")
        c.start()

    customer_id = 1
    try:
        while True:
            time.sleep(random.uniform(1, T1))
            all_current = active_cashiers + reserve_cashiers
            target_cashier = min(all_current, key=lambda c: c.queue.qsize())

            target_cashier.queue.put(f"Клієнт_{customer_id}")
            print(f"--> Прийшов Клієнт_{customer_id}. Черга каси {target_cashier.id}: {target_cashier.queue.qsize()}")
            customer_id += 1

            if target_cashier.queue.qsize() > L_MAX and (len(active_cashiers) + len(reserve_cashiers)) < N:
                new_id = len(active_cashiers) + len(reserve_cashiers) + 1
                reserve = Cashier(new_id, is_reserve=True)
                reserve.start()
                reserve_cashiers.append(reserve)
                print(f"!!! ПАНІКА: Черга велика. Відкрито РЕЗЕРВНУ касу {new_id} !!!")

    except KeyboardInterrupt:
        print("Моделювання зупинено.")


if __name__ == "__main__":
    print(f"Запуск супермаркету. Кас: {M}, Макс черга: {L_MAX}")
    supervisor()