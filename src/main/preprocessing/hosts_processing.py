from typing import List

import pandas as pd

from main.config.config import HOSTS_PATH, HOSTS_PROCESSED_PATH


def get_hosts_list(hosts_path: str) -> List[str]:
    with open(hosts_path, "r") as infile:
        return [line.strip() for line in infile.readlines()]


hosts = get_hosts_list(HOSTS_PATH)
with open(HOSTS_PROCESSED_PATH, "w", encoding='utf-8', newline='\n') as outfile:
    for host in pd.Series(hosts).unique():
        outfile.write(host + '\n')
