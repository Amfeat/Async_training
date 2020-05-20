import socket

URLS = {
    '/': 'Hello index',
    '/blog': 'Hello blog'
}


def parce_request(request):  # разбираем запрос от браузера
    parced = request.split(' ')
    method = parced[0]
    try:
        url = parced[1]
    except:
        return (0, 0)
    cort = (method, url)
    print(cort)
    return cort


def generate_content(code, url):
    if code == 404:
        return "<h1>404</h1><p>URL Not found</p>"
    if code == 405:
        return "<h1>405</h1><p>Method Not allowed</p>"

    return '<h1>{}</h1>'.format(URLS[url])

def generate_headers(method, url):
    if not method == 'GET':
        return ("HTTTP/1.1 405 Method not allowed \n\n", 405)

    if not url in URLS:
        return ("HTTP/1.1 404 Not found \n\n", 404)

    head = "HTTP/1.1 200 OK \n\n"  # + URLS[url]

    return (head, 200)


def generate_response(request):  # генератор ответа

    method, url = parce_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code,url)
    return (headers + body).encode()

    pass


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем переменную субъект, указали какие
    # протоколы будет использовать

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # указываем параметры сокета (НАШ_СОКЕТ, повторное использование адреса, Вкл)

    server_socket.bind(('127.0.0.1', 5000))  # связываем сокет с адресом и портом
    server_socket.listen()  # даем команду слушать заданный порт

    while True:
        client_socket, addr = server_socket.accept()
        # сервер что-то получил (кортеж), присваеваем значения кортежа переменным
        request = client_socket.recv(1024)  # то, что отправил клиент(к-во байт)

        print(request)
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)  # отправка клиенту строки
        client_socket.close()  # закрытие соединения


if __name__ == '__main__':
    run()
