# Round robin/карусель событийный цикл
# Генераторы - это функции, хотя выглядят как списки. у генераторов есть возможность поставить
# выполнение функции на паузу. Функция генератора отдает не только значение, которое он сгенерировал,
# но еще и контроль над выполнением программы. Отдает его в то место, откуда была вызвана функция next()
import socket
from select import select

tasks = []  # список для задач в "карусели"
to_read = {}  # словарь для чтения ключ - сокет, значение - функция для этого сокета
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield 'read', server_socket

        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield 'read', client_socket

        request = client_socket.recv(4096)

        if not request:
            break

        else:
            response = "Hello world\n".encode()
            client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, []) # от словарей берутся ключи

            # добавляем значение ключей в список задач
            for sock in ready_to_read:
                a = to_read.pop(sock)  # just to see how it works
                tasks.append(a)
                print('add read', a)  # just to see how it works
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
                print('add write')


        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
                print(to_write)
        except StopIteration:
            print('done!')


tasks.append(server())
event_loop()
