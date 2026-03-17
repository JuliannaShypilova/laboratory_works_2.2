import socket


def run_client():
    host = '127.0.0.1'
    port = 65432

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        print("Ви підключилися до чату!")

        while True:
            my_msg = input("Ваше повідомлення: ")
            sock.send(my_msg.encode('utf-8'))
            if my_msg.lower() == 'exit': break

            print("Очікування відповіді...")
            other_msg = sock.recv(1024).decode('utf-8')
            print(f"Співрозмовник: {other_msg}")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    run_client()