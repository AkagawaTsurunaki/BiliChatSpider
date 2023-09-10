import json
import logging
import os.path

from config import chat_spider_config as cfg


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
            json.dump(obj=data, fp=file, ensure_ascii=False)

        logging.info(f'💾 {len(data)} records saved.')

    # TODO: 完成数据统计的功能