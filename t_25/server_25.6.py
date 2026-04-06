import socket
import os


def run_server():
    host = '127.0.0.1'
    port = 65432
    upload_dir = '../received_files'

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    print(f"Сервер готовий приймати файли на {host}:{port}...")

    conn, addr = sock.accept()
    print(f"Підключено: {addr}")

    try:
        file_name = conn.recv(1024).decode('utf-8')
        if file_name:
            file_path = os.path.join(upload_dir, file_name)
            with open(file_path, 'wb') as f:
                print(f"Приймаю файл: {file_name}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print(f"Файл успішно збережено у {file_path}")

    except Exception as e:
        print(f"Сталася помилка при прийомі: {e}")
    finally:
        conn.close()
        sock.close()


if __name__ == "__main__":
    run_server()