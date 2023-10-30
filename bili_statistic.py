import os

from config import chat_spider_config as cfg
from core.common import open_json


def print_statistic():
    statistic = []
    total = 0

    if not os.path.exists(cfg.save_path):
        raise FileNotFoundError('Save path is not found, please check your configuration file.')

    for space_id in os.listdir(cfg.save_path):
        path = fr'{cfg.save_path}\{space_id}'
        if os.path.isdir(path):
            data_sum = 0
            for file_name in os.listdir(path):
                data_sum += len(open_json(f'{path}\\{file_name}'))

            statistic.append({
                'space_id': space_id,
                'num': data_sum
            })
            total += data_sum

    print(f'Dataset Statistic Result')
    index = 1
    for item in statistic:
        space_id = item['space_id']
        num = item['num']
        print(f'{index} ({space_id}): {num}')
        index += 1
    print(f'Total: {total}')
    return statistic
