import logging
import time
from multiprocessing import Pool
from random import Random
from typing import List

from alive_progress import alive_bar
from retry import retry
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

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


@retry(NoSuchElementException, tries=2)
def scan_space_by_uid(uid: str, implicitly_wait_time: int = 20):
    driver = DriverInitializer().get_firefox_driver()
    video_list = []
    page_num = 1

    driver.get(f'https://space.bilibili.com/{uid}')
    driver.implicitly_wait(implicitly_wait_time)
    up_name = driver.find_element(By.XPATH,
                                  '/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/span[1]').text

    while True:
        # Open specified page.
        url = f'https://space.bilibili.com/{uid}/video?tid=0&pn={page_num}&keyword=&order=pubdate'
        driver.get(url)
        driver.implicitly_wait(implicitly_wait_time)

        # Slow down the page switching to prevent triggering the captcha.
        time.sleep(Random().randint(a=1, b=3))

        # Find elements that contain information of the video list.
        elems = driver.find_element(By.CLASS_NAME, 'list-list').find_elements(By.CLASS_NAME, 'list-item')
        driver.implicitly_wait(implicitly_wait_time)
        time.sleep(Random().randint(a=3, b=5))

        # If there are no more specified elements to be found, then break.
        if len(elems) == 0:
            break

        # Convert to a video list as Python list.
        for elem in elems:
            bv = elem.get_attribute('data-aid')
            video_list.append(bv)

        # Switch to the next page.
        page_num += 1

    # Close the driver to release resources.
    driver.close()

    return up_name, video_list
