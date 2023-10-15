import json
import logging
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from core.driver_initilizer import DriverInitializer

from config import chat_spider_config as cfg
from core.common import open_page, scroll, xhs_scroll


class ReplyNode:
    def __init__(self, username: str, content: str):
        self.username: str = username
        self.content: str = content
        self.children: List[ReplyNode] = []

    def to_dict(self):
        return {
            'username': self.username,
            'content': self.content,
            'children': [child.to_dict() for child in self.children]
        }

    def add(self, node):
        if node is not None:
            self.children.append(node)

    def find(self, username):
        if self.username == username:
            return self

        for node in self.children:
            result = node.find(username)
            if result is not None:
                return result

        return None


class XhsSingleTaskSpider:

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def __collect(self, post_id: str):

        # Show more comments
        for i in range(1, 30):
            root_comment_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]'
            root_comment_elem = self.driver.find_element(By.XPATH, root_comment_xpath)

            while True:
                show_more_elem = root_comment_elem.find_element(By.CLASS_NAME, 'show-more')
                if show_more_elem is None:
                    break

                show_more_elem.click()
                # scroll(self.driver, count=10, offset=6000)
                time.sleep(2)

    def collect(self, post_id: str):
        open_page(self.driver, f'https://www.xiaohongshu.com/explore/{post_id}')
        xhs_scroll(self.driver, 1)

        # Start collect
        logging.debug(f'🗨️ Collecting replies from the page. ')
        return self.__collect(post_id)


if __name__ == '__main__':

    print(cfg.xhs_save_path)
    driver = DriverInitializer.get_firefox_driver()
    XhsSingleTaskSpider(driver).collect('651280e60000000020000fa4')
    # Command parse
