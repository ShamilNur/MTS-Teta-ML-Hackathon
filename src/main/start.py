import asyncio
import time
from pprint import pprint
from termcolor import cprint

import host_service as service
from main.config.config import HOSTS_PATH, HOSTS_INFO_PATH


def main():
    # Считываем все хосты
    hosts_list = service.get_hosts_list(HOSTS_PATH)

    all_time = time.monotonic()
    batch_size = 50
    for batch in range(0, 10000, batch_size):
        # Для каждого хоста формируем запросы, чтобы получить MIME-тип и статусный код
        loop = asyncio.get_event_loop()
        start = time.monotonic()
        all_time += start
        host_content_types = loop.run_until_complete(service.get_content_types(hosts_list[batch: batch + batch_size]))

        pprint(host_content_types)
        print(batch, "-", batch + batch_size)
        cprint("-" * 40, "green")
        print(round(time.monotonic() - start, 1),
              round(all_time, 1))
        cprint("*" * 40, "green")

        # Сохраняем ответы на запросы в файл
        service.write_data(HOSTS_INFO_PATH, host_content_types)


if __name__ == '__main__':
    main()
