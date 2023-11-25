import logging
import os
import time
from multiprocessing import Pool

from alive_progress import alive_bar
from selenium.webdriver.common.by import By

import config.chat_spider_config as cfg
from core.common import open_page, scroll, find_element
from core.data_structure import ReplyNode
from core.dataset_manager import DatasetManager
from core.driver_initilizer import DriverInitializer
from xiaohongshu.single_task_spider import XhsSingleTaskSpider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_xhs_saved_post_id_list():
    saved_post_id_list = []
    for dirpath, dirnames, filenames in os.walk(cfg.xhs_save_path):
        tmp_saved_post_id_list = [filename.split('.')[0] for filename in filenames]
        if len(tmp_saved_post_id_list) != 0:
            saved_post_id_list += tmp_saved_post_id_list
    return set(saved_post_id_list)


def xhs_exist(post_id: str):
    return post_id in get_xhs_saved_post_id_list()


def __run_single_task(cls: str, post_id: str):
    logging.debug(f'📄 Task (post_id={post_id}) executing...')
    driver = DriverInitializer.get_firefox_driver(False, False)
    data: ReplyNode = XhsSingleTaskSpider(driver).collect(post_id)
    DatasetManager().save_xhs_single_task(cls, post_id, data.to_dict())
    driver.close()
    driver.quit()
    print(f'📄 Task (post_id={post_id}) completed: {len(data)} records saved.')


def __load(cls: str, post_id_list: list, callback):
    pool = Pool(cfg.max_parallel_job_num)

    for post_id in post_id_list:
        pool.apply_async(func=__run_single_task, args=(cls, post_id), callback=callback)
        time.sleep(8)

    pool.close()
    pool.join()


def __collect_by_channel_id(driver, channel_id: str, thr: int = 1000):
    post_id_set = []
    try:
        url = f'https://www.xiaohongshu.com/explore?channel_id={channel_id}'
        open_page(driver, url, 0)
        scroll(driver, 3000, 4, 1)

        for i in range(1, 40):
            post_id_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[{i}]/div/a[1]'
            like_count_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[{i}]/div/div/div/span/span[2]'
            post_id_elem = find_element(driver, By.XPATH, post_id_xpath, wait_time=2, sleep_time=0,
                                        suppress_exception=False)
            like_count_elem = find_element(driver, By.XPATH, like_count_xpath, wait_time=2, sleep_time=0,
                                           suppress_exception=True)
            like = __convert_str_to_num(like_count_elem.text)
            # If like count is less than the threshold given by user,
            # then we just skip this post for performance
            if like < thr:
                continue
            post_id_set.append(post_id_elem.get_attribute('href').split('/')[-1])

    except Exception:
        pass

    post_id_set = set(post_id_set) - get_xhs_saved_post_id_list()
    return post_id_set


def __convert_str_to_num(num_str: str):
    if num_str in [None, '', ' ']:
        return 0
    if num_str[-1].lower() == 'w':
        return int(num_str[:-1]) * 10000
    if num_str[-1] == '+':
        return int(num_str[:-1])
    return int(num_str)


def collect_by_post_id(cls: str, post_id: str):
    if xhs_exist(post_id):
        return
    __run_single_task(cls, post_id)


def collect_by_post_id_list(cls: str, post_id_list: list):
    post_id_list = list(set(post_id_list) - set(get_xhs_saved_post_id_list()))
    print(f'⛰️ Tasks: {len(post_id_list)}')

    with alive_bar(len(post_id_list)) as total_bar:
        __load(cls, post_id_list, lambda *args: total_bar())


def collect_by_channel_id(cls: str, channel_id: str, task_count: int = 3, thr: int = 1000):
    driver = DriverInitializer.get_firefox_driver(stylesheet=True)
    post_id_list = []
    for _ in range(task_count):
        post_id_list += list(__collect_by_channel_id(driver, channel_id, thr))
        time.sleep(5)
        driver.refresh()

    driver.close()
    driver.quit()

    collect_by_post_id_list(cls, post_id_list)
