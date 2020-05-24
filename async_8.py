# вариант обычного(синхронного) скачивания файлов. время выполнения 9-12 сек


import requests
from time import time
# url = 'https://loremflickr.com/320/240'


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r
def write_file(responce):
    filename = responce.url.split('/')[-1]
    with open(filename, 'wb',) as file:
        file.write(responce.content)

def main():
    t0 = time()

    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

    print(time()-t0)

if __name__ == '__main__':
    main()