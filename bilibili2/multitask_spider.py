import logging
from typing import List

from alive_progress import alive_bar

from core.common import multiprocess
from core.dataset_manager import DatasetManager
from core.driver_initilizer import DriverInitializer

from single_task_spider import SingleTaskSpider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def __run_single_task(bv: str, uid: str):
    logging.debug(f'📄 Task (bv={bv}) executing...')
    driver = DriverInitializer.get_firefox_driver()
    data = SingleTaskSpider(driver).collect(bv)
    DatasetManager().save_bili_single_task(uid=uid, bv=bv, data=data)
    driver.close()
    driver.quit()
    logging.info(f'📄 Task (bv={bv}) completed: {len(data)} records saved.')


def collect_by_bv_list(uid: str, bv_list: List[str]):
    with alive_bar(len(bv_list)) as total_bar:
        multiprocess(job_list=bv_list, func=__run_single_task, args=tuple(uid), callback=lambda *arg: total_bar())
