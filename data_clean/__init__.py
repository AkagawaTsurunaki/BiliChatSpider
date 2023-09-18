import copy
import json
import multiprocessing
import os

from sklearn.model_selection import train_test_split
from filter.reply_symbol_filter import reply_symbol_filter, reply_symbol_filter_2
from filter.encoding_filter import encoding_filter
from filter.blank_filter import blank_filter

import config.chat_spider_config as cfg


def split_list(lst, num_parts):
    part_length = len(lst) // num_parts
    divided_list = [lst[i * part_length: (i + 1) * part_length] for i in range(num_parts)]
    if len(lst) % num_parts != 0:
        divided_list[-1].extend(lst[num_parts * part_length:])

    return divided_list


def process_array_in_parallel(data, num_processes, func):
    chunk_size = len(data) // num_processes

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = []

        for i in range(num_processes):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_processes - 1 else len(data)
            result = pool.apply_async(func, args=(copy.deepcopy(data[start:end]),))
            results.append(result)

        processed_array = []
        for result in results:
            processed_array.extend(result.get())

        return processed_array


def run():
    core_num = 24

    save_path = fr'{cfg.save_path}'

    if not os.path.exists(save_path):
        raise NotADirectoryError('Dataset path is not found.')

    data = list()

    for folder in os.listdir(save_path):
        folder_path = fr'{save_path}\{folder}'
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                with open(fr'{folder_path}\{file_name}', encoding='utf-8', mode='r') as file:
                    replies_in_file = json.load(fp=file)
                    for reply in replies_in_file:
                        data.append(reply)

    print(f'Original data size: {len(data)}')

    # Maintain data with UFT-8 and the confidence of the encoding is greater than 99
    data = process_array_in_parallel(data, core_num, func=encoding_filter)
    print(f'Non-UTF-8 excluded data size: {len(data)}')

    data = process_array_in_parallel(data, core_num, func=reply_symbol_filter)
    print(f'Reply-symbol excluded data size: {len(data)}')

    data = process_array_in_parallel(data, core_num, func=blank_filter)
    print(f'Blank replies excluded data size: {len(data)}')

    data = process_array_in_parallel(data, core_num, func=reply_symbol_filter_2)
    print(f'Blank replies excluded data size: {len(data)}')

    print(f'Final data size: {len(data)}')

    train_data, val_data = train_test_split(data, test_size=0.01, random_state=114514)
    with open(file=fr'.\train.json', mode='w', encoding='utf-8') as file:
        json.dump(ensure_ascii=False, fp=file, obj=data, indent=4)
    # with open(file=fr'.\dev.json', mode='w', encoding='utf-8') as file:
    #     json.dump(ensure_ascii=False, fp=file, obj=val_data, indent=4)


if __name__ == '__main__':
    run()
