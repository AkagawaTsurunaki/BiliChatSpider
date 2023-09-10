import json
import logging
import os.path

import history
from config import chat_spider_config as cfg


class DatasetManager:

    def __init__(self, dataset_save_path):
        self.log = self.__init_logger()
        self.dataset_save_path = dataset_save_path
        if not os.path.exists(self.dataset_save_path):
            raise NotADirectoryError(f'无法找到数据集保存路径“{self.dataset_save_path}”，请检查您的配置文件。')
        self.space_list = []
        self.history = []
        self.__init_space_list()

    @staticmethod
    def save_task(self, up_name: str, uid: str, bv: str, data):
        if not os.path.exists(cfg.save_path):
            os.makedirs(cfg.save_path)

        # Write in json file
        path = fr'{cfg.save_path}\{bv}.json'

        with open(path, 'w', encoding='utf-8') as file:
            # 将data_set以json格式保存到json文件中
            json.dump(data, file, ensure_ascii=False)



        logging.info(f'💾 {len(data)} records saved.')

    def __init_space_list(self):

        for up_data in os.listdir(self.dataset_save_path):
            if os.path.isdir(f'{self.dataset_save_path}\\{up_data}'):
                self.space_list.append(up_data)

    def get_saved_video_list_by_space_id(self, space_id: str):
        saved_video_list = []
        if space_id in self.space_list:
            path = f'{self.dataset_save_path}\\{space_id}'
            if os.path.exists(path):
                for file_name in os.listdir(path):
                    saved_video_list.append("".join(file_name.split('.')[0:-1]))
        return saved_video_list

    def print_statistic(self):
        statistic = []
        total = 0
        for space_id in os.listdir(self.dataset_save_path):
            path = f'{self.dataset_save_path}\\{space_id}'
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
            print(f'{index} {history.get_name(space_id)} ({space_id}): {num}')
            index += 1
        print(f'Total: {total}')
        return statistic


if __name__ == '__main__':
    DatasetManager(dataset_save_path='./dataset').print_statistic()
