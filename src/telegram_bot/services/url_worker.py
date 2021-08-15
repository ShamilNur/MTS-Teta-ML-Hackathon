from random import randint


async def url_worker(url: str) -> str:
    url = url.strip()
    answer = ["Нетехнический", "Технический"]
    return answer[randint(0, 1)]
