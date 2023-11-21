import json
import logging
import os.path
from typing import List, Set

from config import chat_spider_config as cfg
from core.common import open_json, save_json


class DatasetManager:

    def __init__(self):
        if not os.path.exists(cfg.save_path):
            os.makedirs(cfg.save_path)
        if not os.path.exists(cfg.xhs_save_path):
            os.makedirs(cfg.xhs_save_path)

    @staticmethod
    def save_bili_single_task(uid: str, bv: str, data):
        # Prevent from raising exception if the folder is not created
        path = fr'{cfg.save_path}\{uid}'
        if not os.path.exists(path):
            os.makedirs(path)
        # Save the data by saving as json file
        with open(file=fr'{path}\{bv}.json', mode='w', encoding='utf-8') as file:
            json.dump(obj=data, fp=file, ensure_ascii=False, indent=4)

    @staticmethod
    def save_xhs_single_task(cls: str, page_id: str, data):

        # Prevent from raising exception if the folder is not created
        path = fr'{cfg.xhs_save_path}\{cls}'
        if not os.path.exists(path):
            os.makedirs(path)
        # Save the data by saving as json file
        path = fr'{path}\{page_id}.json'
        if save_json(path, data):
            logging.debug(f'{path} is saved.')

    @staticmethod
    def xhs_statistic():
        total = 0
        for filepath in DatasetManager.__load(cfg.xhs_save_path):
            root = open_json(filepath)
            total += len(root)
        return total

    @staticmethod
    def bili2_statistic():
        total = 0
        for filepath in DatasetManager.__load(cfg.save_path):
            root = open_json(filepath)
            total += len(root)
        return total

    def bili_exist(self, bv) -> (bool, str | None):
        return self.__exists(cfg.save_path, bv)

    def xhs_exist(self, post_id) -> (bool, str | None):
        return self.__exists(cfg.xhs_save_path, post_id)

    def xhs_existed_bv_list(self):
        result = set()
        for dirpath, dirnames, filenames in os.walk(cfg.save_path):
            for filename in filenames:
                bv = filename.split('.')[-2]
                if bv[:2].lower() == 'bv':
                    result.add(bv)
        return result


    @staticmethod
    def __exists(path: str, filename: str) -> (bool, str | None):
        """
        Check if the file with the specified filename already exists.
        :param path: Dataset save path.
        :param filename: Name of the file without its suffix.
        :return: (True, fullpath) if file exists, (False, None) if file dose not exists.
        """

        for pair in DatasetManager.__map(path):
            if pair['filename'] == filename:
                return True, pair['fullpath']

        return False, None

    @staticmethod
    def __map(path: str) -> List:
        all_file = DatasetManager.__load(path)
        result = list()
        for full_file_path in all_file:
            result += [{
                'fullpath': full_file_path,
                'filename': full_file_path.split('.')[-2]
            }]
        return result

    @staticmethod
    def __load(path: str) -> Set[str]:
        result = set()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename == 'history.json':
                    continue
                result.add(os.path.join(dirpath, filename))

        return result
