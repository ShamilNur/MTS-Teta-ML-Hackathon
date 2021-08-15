import asyncio
import time
from pprint import pprint
from termcolor import cprint
from tqdm import tqdm

import host_service as service
from main.config.config import HOSTS_PROCESSED_PATH, HOSTS_INFO_PATH, DIR_DATA


def main():
    # Считываем все хосты
    hosts_list = service.get_hosts_list(HOSTS_PROCESSED_PATH)

    # Для каждого хоста формируем запросы, чтобы получить MIME-тип и статусный код
    batch_size = 150
    for batch in tqdm(range(7950, 199_944, batch_size)):
        loop = asyncio.get_event_loop()
        start = time.monotonic()
        host_content_types = loop.run_until_complete(service.get_content_types(
            hosts_list[batch: batch + batch_size])
        )

        pprint(host_content_types)
        print(batch, "-", batch + batch_size)
        cprint("-" * 40, "green")
        print("This batch:", round(time.monotonic() - start, 1))
        cprint("*" * 40, "green")

        # Сохраняем ответы на запросы в файл
        service.write_data(HOSTS_INFO_PATH, host_content_types)


if __name__ == '__main__':
    main()
