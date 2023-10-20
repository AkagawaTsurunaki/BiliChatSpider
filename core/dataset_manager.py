import json
import logging
import os.path

from config import chat_spider_config as cfg
from core.common import open_json


class DatasetManager:

    def __init__(self):
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
            json.dump(obj=data, fp=file, ensure_ascii=False, indent=4)

    def save_xhs_single_task(self, cls: str, page_id: str, data):

        # Prevent from raising exception if the folder is not created
        path = fr'{cfg.xhs_save_path}\{cls}'
        if not os.path.exists(path):
            os.makedirs(path)
        # Save the data by saving as json file
        path = fr'{path}\{page_id}.json'
        if self.save_json(path, data):
            logging.debug(f'{path} is saved.')

    @staticmethod
    def save_json(path: str, obj):
        try:
            with open(file=path, mode='w', encoding='utf-8') as file:
                json.dump(obj=obj, fp=file, ensure_ascii=False, indent=4)
                return True
        except IOError:
            return False

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

    @staticmethod
    def __get_xhs_saved_file_name_list(path=cfg.xhs_save_path):
        file_path_list = []
        for dirpath, _, filenames in os.walk(path, topdown=True):
            file_path_list += [os.path.join(dirpath, filename) for filename in filenames]
        return file_path_list

    @staticmethod
    def print_xhs_statistic():
        print(f'Dataset (Xiaohongshu) Statistic Result')
        total = 0
        for filepath in DatasetManager.__get_xhs_saved_file_name_list():
            root = open_json(filepath)
            total += len(root)
        print(f'Total: {total}')
        return total
