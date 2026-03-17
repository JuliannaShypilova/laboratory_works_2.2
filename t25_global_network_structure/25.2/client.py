import socket


def run_client():
    host = '127.0.0.1'
    port = 65432

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        user_input = input("Введіть арифметичний вираз (наприклад, 2 + 2 * 2): ")
        if user_input.strip() == "":
            print("Ви ввели порожній рядок!")
        else:
            sock.send(user_input.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            print(f"Відповідь сервера: {response}")

    except ConnectionRefusedError:
        print("Помилка: Не вдалося підключитися до сервера. Перевірте, чи запущено server.py")
    except Exception as e:
        print(f"Сталася помилка: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    run_client()