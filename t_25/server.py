import socket


def check_expression(text):
    try:
        eval(text)
        return "Синтаксис правильний"
    except SyntaxError:
        return "Помилка: Неправильний синтаксис!"
    except NameError:
        return "Помилка: Вираз містить невідомі змінні!"
    except Exception as e:
        return f"Помилка: {e}"


def run_server():
    host = '127.0.0.1'
    port = 65432

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    print(f"Сервер запущено на {host}:{port}. Очікування...")

    conn, addr = sock.accept()
    print(f"Підключено клієнта: {addr}")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Отримано для перевірки: {data}")
            result = check_expression(data)
            conn.send(result.encode('utf-8'))
    except Exception as e:
        print(f"Виникла помилка під час роботи: {e}")
    finally:
        conn.close()
        sock.close()
        print("З'єднання закрито.")


if __name__ == "__main__":
    run_server()