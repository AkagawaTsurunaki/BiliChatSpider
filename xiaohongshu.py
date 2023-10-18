import logging
import time
from typing import List
import re

from selenium.common import NoSuchElementException
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

reply_regex = re.compile('回复\s(.*)\s*[：:]\s*(.*)')
class XhsSingleTaskSpider:

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def __get_root(self):
        username_elem = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div/div[1]/a[2]')
        title_elem = self.driver.find_element(By.XPATH, '//*[@id="detail-title"]')
        detail_elem = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/span[1]')
        self.driver.implicitly_wait(1)
        root = ReplyNode(username=username_elem.text, content=title_elem.text + detail_elem.text)
        return root

    def __refactor(self, root: ReplyNode):
        for second_child in root.children:
            duplicate_children = second_child.children.copy()
            second_child.children = []
            for i, third_child in enumerate(duplicate_children):
                result = reply_regex.search(third_child.content)
                if result is None:
                    second_child.children.append(third_child)
                    continue
                reply_to = result.group(1)
                third_child.content = result.group(2)

                appended = False
                for recent_child in duplicate_children[i::-1]:
                    if recent_child.username == reply_to:
                        recent_child.children.append(third_child)
                        appended = True
                        break
                if not appended:
                    second_child.children.append(third_child)


    def __deep(self, root: ReplyNode, i, j):
        reply_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[5]/div/div[{j}]/div/div[2]/div[1]/div/a'
        reply_name_elem = self.driver.find_element(By.XPATH, reply_name_xpath)

        reply_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[5]/div/div[{j}]/div/div[2]/div[2]'
        reply_content_elem = self.driver.find_element(By.XPATH, reply_content_xpath)

        self.driver.implicitly_wait(1)

        node = ReplyNode(username=reply_name_elem.text, content=reply_content_elem.text)
        root.add(node)

        self.__refactor(node)

        return root

    def show_more(self, comment_elem):
        try:
            while True:
                show_more_elem = comment_elem.find_element(By.CLASS_NAME, 'show-more')
                if show_more_elem is None:
                    break
                show_more_elem.click()
                # scroll(self.driver, count=10, offset=6000)
                time.sleep(1)
        except NoSuchElementException:
            pass

    def __collect(self, root: ReplyNode):
        # Show more comments
        # TODO: Need more tests, remember change 2 to a var
        for i in range(1, 2):
            comment_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]'
            comment_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[2]'
            comment_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[1]/div/a'

            comment_name_elem = self.driver.find_element(By.XPATH, comment_name_xpath)
            comment_elem = self.driver.find_element(By.XPATH, comment_xpath)
            comment_content_elem = self.driver.find_element(By.XPATH, comment_content_xpath)
            self.driver.implicitly_wait(1)

            comment = ReplyNode(username=comment_name_elem.text, content=comment_content_elem.text)
            root.add(comment)

            self.show_more(comment_elem)

            # Deep Search
            try:
                for j in range(1, 100):
                    comment = self.__deep(comment, i, j)
            except NoSuchElementException:
                pass

            xhs_scroll(self.driver, 1)
            print(root.to_dict())

    def collect(self, post_id: str):
        open_page(self.driver, f'https://www.xiaohongshu.com/explore/{post_id}')

        # Start collect
        logging.debug(f'🗨️ Collecting replies from the page. ')
        root = self.__get_root()
        return self.__collect(root)


if __name__ == '__main__':
    print(cfg.xhs_save_path)
    driver = DriverInitializer.get_firefox_driver()
    # TODO: Change it to a var
    XhsSingleTaskSpider(driver).collect('651280e60000000020000fa4')
    # Command parse
