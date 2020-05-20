import socket
from select import select  # функция для мониторинга изменений состояния файловых объектов и сокетов

# .fileno()  метод, который возвращает файловый дескриптор (просто номер файла, целое число)


to_monitor = []  # список того, что будем мониторить
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
    to_monitor.append(client_socket)


#       send_message(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)

    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # аргументы функции: чтение, запись, ошибки.
        # Можно ставить пустой список
        # Функция делает выборку из списков, проверяя готовность объекта для чтения\записи. Если они готовы, создает
        # соотвествующие списки.
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)  # заполняем список для мониторинга
    event_loop()
