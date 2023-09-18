import json
import os
from json import JSONDecodeError

import config.chat_spider_config as cfg


class __History:

    def __init__(self):
        path = fr'{cfg.save_path}\history.json'

        if not os.path.exists(path):
            os.makedirs(path)
        self.history = []

    def __load(self):
        path = fr'{cfg.save_path}\history.json'
        try:
            with open(file=path, encoding='utf-8', mode='r') as file:
                self.history = json.load(file)
        except JSONDecodeError:
            pass

    def is_job_completed(self, uid: str):
        self.__load()
        for history_item in self.history:
            if history_item['uid'] == uid:
                return history_item['is_job_completed']

    def get_uncompleted_tasks(self, uid: str):
        self.__load()
        for history_item in self.history:
            if history_item['uid'] == uid:
                return history_item['uncompleted_tasks']
        return []

    def create_job(self, up_name, uid, uncompleted_tasks):
        self.__load()
        job = {
            'up_name': up_name,
            'uid': uid,
            'is_job_completed': False,
            'completed_tasks': [],
            'uncompleted_tasks': uncompleted_tasks,
        }
        self.history.append(job)
        self.__save_history()

    def single_task_completed(self, uid: str, bv: str):
        self.__load()
        for history_item in self.history:
            if history_item['uid'] == uid:
                # Remove bv from uncompleted_tasks
                for uncompleted_task in history_item['uncompleted_tasks']:
                    if uncompleted_task == bv:
                        history_item['uncompleted_tasks'].remove(bv)
                # Add bv into completed_tasks
                history_item['completed_tasks'].append(bv)
                # Check if all tasks completed
                history_item['is_job_completed'] = len(history_item['uncompleted_tasks']) == 0
        self.__save_history()

    def __save_history(self):
        with open(file=fr'{cfg.save_path}\history.json', encoding='utf-8', mode='w') as file:
            if len(self.history) == 0:
                self.history = []
            json.dump(fp=file, ensure_ascii=False, obj=self.history)


HistoryManager = __History()
