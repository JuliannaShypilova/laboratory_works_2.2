import socket
import os


def run_client():
    host = '127.0.0.1'
    port = 65432
    file_to_send = input("Введіть назву файлу для відправки (наприклад, test.txt): ")

    if not os.path.exists(file_to_send):
        print("Помилка: Такого файлу не існує!")
        return

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(file_to_send.encode('utf-8'))

        import time
        time.sleep(0.1)
        with open(file_to_send, 'rb') as f:
            print(f"Відправляю {file_to_send}...")
            sock.sendall(f.read())

        print("Відправку завершено.")

    except ConnectionRefusedError:
        print("Сервер не запущено!")
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    run_client()