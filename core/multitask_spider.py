import logging
import time
from multiprocessing import Pool

import config.chat_spider_config as cfg
from core.dataset_manager import DatasetManager
from core.driver_initilizer import DriverInitializer
from core.history_manager import HistoryManager
from core.single_task_spider import SingleTaskSpider


def __run_single_task(history: HistoryManager, uid: str, bv: str):
    logging.debug(f'Task {bv} executing...')
    driver = DriverInitializer.get_firefox_driver()
    data = SingleTaskSpider(driver).get_reply_records(bv)
    DatasetManager().save_single_task(uid=uid, bv=bv, data=data)
    history.single_task_completed(uid=uid, bv=bv)
    driver.close()
    driver.quit()
    logging.debug(f'Task {bv} completed.')

def run(uid: str):

    # If the job is completed then return straightly
    if HistoryManager.is_job_completed(uid):
        return

    # If the job is not completed,
    pool = Pool(cfg.max_parallel_job_num)  # 创建一个5个进程的进程池
    # Get the uncompleted bv list.
    for bv in HistoryManager.get_uncompleted_tasks(uid):
        pool.apply_async(func=__run_single_task, args=(HistoryManager, uid, bv))
        time.sleep(3)

    pool.close()
    pool.join()
