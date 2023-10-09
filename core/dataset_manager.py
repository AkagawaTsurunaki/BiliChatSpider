import json
import logging
import os.path

from config import chat_spider_config as cfg


class DatasetManager:

    def __init__(self):
        logging.debug(f'permissions.default.image is set to 2, images in the website will not be loaded.')
        if not os.path.exists(cfg.save_path):
            os.makedirs(cfg.save_path)

    @staticmethod
    def save_single_task(uid: str, bv: str, data):
        # Prevent from raising exception if the folder is not created
        path = fr'{cfg.save_path}\{uid}'
        if not os.path.exists(path):
            os.makedirs(path)
        # Save the data by saving as json file
        with open(file=fr'{path}\{bv}.json', mode='w', encoding='utf-8') as file:
            json.dump(obj=data, fp=file, ensure_ascii=False)

        logging.info(f'💾 {len(data)} records saved.')

    @staticmethod
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
                    with open(f'{path}\\{file_name}', 'r', encoding='utf-8') as file:
                        data_list = json.load(fp=file)
                        data_sum += len(data_list)

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
