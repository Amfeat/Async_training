import socket
import selectors  # модуль, содержит разные селекторы. можно проверить какой будет по умолчанию из shell

selector = selectors.DefaultSelector()  # задаем функцию для использования дефолтного селектора


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

#  регистрация серверного сокета.(объект=сокет, событие для отслеживания = чтение, связанные данные = объект функции)
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
#  регистрация серверного сокета.(объект=сокет, событие для отслеживания = чтение, связанные данные = объект функции)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)





def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)

    else:
        selector.unregister(fileobj=client_socket)
        client_socket.close()


def event_loop():
    while True:

        events = selector.select()  # (key, events)

        # key - selectorkey(кортеж) связывает сокет, ожидаемое событие, данные (т.е. свяанную функцию)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)  # вызываем accept_connection(server_socket) или send_message(client_socket)

        pass


if __name__ == '__main__':
    server()
    event_loop()
