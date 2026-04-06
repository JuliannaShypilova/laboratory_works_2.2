import socket


def run_server():
    host = '127.0.0.1'
    port = 65432

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(2)
    print("Сервер чату запущено. Очікування двох клієнтів...")

    conn1, addr1 = sock.accept()
    print(f"Клієнт 1 підключився: {addr1}")

    conn2, addr2 = sock.accept()
    print(f"Клієнт 2 підключився: {addr2}")

    try:
        while True:
            msg1 = conn1.recv(1024)
            if not msg1: break
            print(f"Клієнт 1 пише: {msg1.decode('utf-8')}")
            conn2.send(msg1)

            msg2 = conn2.recv(1024)
            if not msg2: break
            print(f"Клієнт 2 пише: {msg2.decode('utf-8')}")
            conn1.send(msg2)
    except Exception as e:
        print(f"Зв'язок розірвано: {e}")
    finally:
        conn1.close()
        conn2.close()
        sock.close()


if __name__ == "__main__":
    run_server()