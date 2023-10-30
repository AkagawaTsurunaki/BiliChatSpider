import json
import logging
import random
import time
from multiprocessing import Pool

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
import config.chat_spider_config as cfg
from core.data_structure import ReplyNode


def find_element(driver: WebDriver, by: By.ID, value: str, wait_time: float = 2, sleep_time: float = 2,
                 suppress_exception: bool = False):
    try:
        elem = driver.find_element(by, value)
        driver.implicitly_wait(wait_time)
        time.sleep(sleep_time)
        return elem, None
    except NoSuchElementException as e:
        if suppress_exception:
            return None, e
        raise e


def open_json(path: str) -> ReplyNode | None:
    try:
        with open(file=path, mode='r', encoding='utf-8') as file:
            dat = json.load(fp=file)
            return ReplyNode.from_dict(dat)
    except IOError:
        return None


def save_json(path: str, obj) -> bool:
    try:
        with open(file=path, mode='w', encoding='utf-8') as file:
            json.dump(obj=obj, fp=file, ensure_ascii=False, indent=4)
            return True
    except IOError:
        return False


def open_page(driver, url: str, wait_time=5):
    # Open specified page
    driver.get(url)

    # Wait for loading of resources
    driver.implicitly_wait(wait_time)
    time.sleep(random.Random().random() * wait_time)
    logging.debug(f'🌐 Successfully open the page at {url}". ')


def is_bv_valid(bv: str) -> bool:
    if bv == '' or bv is None:
        return False
    if len(bv) != 12:
        return False
    if bv[:2] != 'BV':
        return False
    return True


def scroll(driver, offset, count=1, sleep_time=0.7):
    # Control the page to scroll
    for _ in range(count):
        time.sleep(sleep_time)
        driver.execute_script(f'window.scrollBy(0,{offset})')
    logging.debug(
        f'🖱️ Total number of pixels of scrolling is {count * offset}. ')


def xhs_scroll(driver: WebDriver, count=10, wait_time=1):
    # Control the page to scroll
    for _ in range(count):
        js = """
        const elem = document.querySelector('html body div#app div#global.layout.limit div.main-container div.with-side-bar.main-content div.outer-link-container div#noteContainer.note-container div.interaction-container div.note-scroller')
        elem.scrollTop = elem.scrollHeight 
        """
        driver.execute_script(js)
        time.sleep(wait_time)


def multiprocess(job_list: list,
                 func, callback, args: tuple | None = None,
                 delay: float = 5,
                 max_parallel_job_num: int = cfg.max_parallel_job_num):
    pool = Pool(max_parallel_job_num)

    for job in job_list:
        if args is None:

            pool.apply_async(func=func, callback=callback)
        else:
            pool.apply_async(func=func, args=(job,) + args, callback=callback)
        time.sleep(delay)

    pool.close()
    pool.join()
