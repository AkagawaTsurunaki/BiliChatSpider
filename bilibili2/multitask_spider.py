import logging
import time
from multiprocessing import Pool
from typing import List

from alive_progress import alive_bar

from bilibili2.single_task_spider import SingleTaskSpider
from config import chat_spider_config as cfg
from core.dataset_manager import DatasetManager
from core.driver_initilizer import DriverInitializer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def __run_single_task(uid: str, bv: str):
    logging.debug(f'📄 Task (bv={bv}) executing...')
    driver = DriverInitializer.get_firefox_driver()
    data = SingleTaskSpider(driver).collect(bv)
    DatasetManager().save_bili_single_task(uid=uid, bv=bv, data=data.to_dict())
    driver.close()
    driver.quit()
    logging.info(f'📄 Task (bv={bv}) completed: {len(data)} records saved.')


def __load(uid: str, bv_list: list, callback):
    pool = Pool(cfg.max_parallel_job_num)

    for post_id in bv_list:
        pool.apply_async(func=__run_single_task, args=(uid, post_id), callback=callback)
        time.sleep(5)

    pool.close()
    pool.join()


def collect_by_bv_list(uid: str, bv_list: List[str]):
    with alive_bar(len(bv_list)) as total_bar:
        __load(uid, bv_list, lambda *arg: total_bar())
