import logging
import random
import time

from selenium.webdriver.firefox.webdriver import WebDriver


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


def xhs_scroll(driver: WebDriver, count=10, wait_time=1):
    # Control the page to scroll
    for _ in range(count):
        js = """
        const elem = document.querySelector('html body div#app div#global.layout.limit div.main-container div.with-side-bar.main-content div.outer-link-container div#noteContainer.note-container div.interaction-container div.note-scroller')
        elem.scrollTop = elem.scrollHeight 
        """
        driver.execute_script(js)
        time.sleep(wait_time)
