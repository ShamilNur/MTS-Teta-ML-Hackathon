import sys
import csv

import aiohttp
import asyncio

from typing import List, Tuple


def get_hosts_list(hosts_path: str) -> List[str]:
    with open(hosts_path, "r") as infile:
        return [line.strip() for line in infile.readlines()]


async def get_content_types(hosts: List) -> List[Tuple[str, str, str]]:
    host_types: List[Tuple[str, str, str]] = list()

    async def load_content_types(host: str):
        # print(f"Task with host: {host}...")
        async with aiohttp.ClientSession(conn_timeout=5) as session:
            response = None
            try:
                # Пробуем установить https-соединиение
                async with session.get("https://" + host) as https_resp:
                    response = https_resp
            except BaseException as e:
                print("Ошибка в https блоке:", e)
                try:
                    # При неуспешном https, открываем http-соединение
                    async with session.get("http://" + host) as http_resp:
                        response = http_resp
                except BaseException as e:
                    # Не установилось соединение по https и http. Считаем хост техническим
                    print("Ошибка в http блоке:", e)

            status: str = ""
            content_type: str = ""

            if response:
                try:
                    status = str(response.status)
                    content_type = response.headers["Content-Type"]
                except KeyError:
                    # Ответы некоторых хостов могут не содержат заголовок "Content-Type"
                    print(f"{host}, Error: {sys.exc_info()[0]}")

            host_types.append((host, status, content_type))
            print(f"{host}, Status: {status}, Content-type: {content_type}")

    # Формируем корутины (сопрограммы)
    async def create_content_types_coroutines():
        coroutines = [load_content_types(host) for host in hosts]
        await asyncio.gather(*coroutines)

    await create_content_types_coroutines()

    return host_types


def write_data(
        file_path: str,
        host_content_types: List[Tuple[str, str, str]]
) -> None:
    # Запишем всю информацию в файл
    with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        for host, status, content_type in host_content_types:
            writer.writerow((host, status, content_type))
