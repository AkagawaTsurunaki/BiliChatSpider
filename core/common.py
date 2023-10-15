import logging
import random
import time


def open_page(driver, url: str, wait_time=5):
    # Open specified page
    driver.get(url)

    # Wait for loading of resources
    driver.implicitly_wait(wait_time)
    time.sleep(random.Random().random() * wait_time)
    logging.debug(f'🌐 Successfully open the page at {url}". ')


def scroll(driver, offset, count=1):
    # Control the page to scroll
    for _ in range(count):
        time.sleep(0.7)
        driver.execute_script(f'window.scrollBy(0,{offset})')
    logging.debug(
        f'🖱️ Total number of pixels of scrolling is {count * offset}. ')
