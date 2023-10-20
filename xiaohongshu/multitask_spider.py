import logging
import os
import time
from multiprocessing import Pool

from selenium.webdriver.common.by import By

import config.chat_spider_config as cfg
from core.common import open_page, scroll
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
    driver = DriverInitializer.get_firefox_driver()
    data: ReplyNode = XhsSingleTaskSpider(driver).collect(post_id)
    DatasetManager().save_xhs_single_task(cls, post_id, data.dict())
    driver.close()
    driver.quit()
    logging.info(f'📄 Task (post_id={post_id}) completed: {len(data)} records saved.')


def __load(cls: str, post_id_list: list):
    pool = Pool(cfg.max_parallel_job_num)

    for post_id in post_id_list:
        pool.apply_async(func=__run_single_task, args=(cls, post_id))
        time.sleep(3)

    pool.close()
    pool.join()


def collect_by_channel_id(cls: str, channel_id: str):
    url = f'https://www.xiaohongshu.com/explore?channel_id={channel_id}'
    driver = DriverInitializer.get_firefox_driver(stylesheet=True)
    open_page(driver, url, 0)
    scroll(driver, 3000, 4)

    post_id_list = []
    for i in range(1, 10):
        post_id_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[{i}]/div/a[1]'
        # f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[1]/div/div/a'
        # f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[3]/section[2]/div/div/a'
        driver.implicitly_wait(1)
        post_id_elem = driver.find_element(By.XPATH, post_id_xpath)
        post_id_list.append(post_id_elem.get_attribute('href').split('/')[-1])

    driver.close()
    driver.quit()

    post_id_list = set(post_id_list) - get_xhs_saved_post_id_list()

    __load(cls, list(post_id_list))
