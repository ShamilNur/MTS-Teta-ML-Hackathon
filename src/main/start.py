import asyncio
import time
from pprint import pprint

import host_service as service
from main.config.config import HOSTS_PATH, HOSTS_INFO_PATH


def main():
    # Считываем все хосты
    hosts_list = service.get_hosts_list(HOSTS_PATH)

    # Для каждого хоста формируем запросы, чтобы получить MIME-тип и статусный код
    loop = asyncio.get_event_loop()
    start = time.monotonic()
    host_content_types = loop.run_until_complete(service.get_content_types(hosts_list[:10000]))
    pprint(host_content_types)
    print(len(host_content_types))
    print(time.monotonic() - start)

    # Сохраняем ответы на запросы в файл
    service.write_data(HOSTS_INFO_PATH, host_content_types)


if __name__ == '__main__':
    main()
