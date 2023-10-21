import json
import logging
import random
import re
import time
from typing import Type

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from core.common import open_page, xhs_scroll, find_element
from core.data_structure import ReplyNode
from data_clean.filter.at_filter import at_filter


class XhsSingleTaskSpider:

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.reply_regex = re.compile('回复\s(.*)\s*[：:]\s*(.*)')

    def __get_root(self):
        username_xpath = '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[1]/div/div[1]/a[2]/span'
        title_xpath = '//*[@id="detail-title"]'
        detail_xpath = '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/span[1]'

        username_elem, e = find_element(self.driver, By.XPATH, username_xpath, 2, 0, False)
        title_elem, e = find_element(self.driver, By.XPATH, title_xpath, 2, 0, False)
        detail_elem, e = find_element(self.driver, By.XPATH, detail_xpath, 2, 0, True)

        username_txt = username_elem.text
        content_txt = title_elem.text if title_elem is not None else '' + detail_elem.text if detail_elem is not None else ''

        root = ReplyNode(username_txt, content_txt)
        print(json.dumps(root.to_dict(), ensure_ascii=False))

        return root

    def __refactor(self, root: ReplyNode):
        for second_child in root.children:
            duplicate_children = second_child.children.copy()
            second_child.children = []
            for i, third_child in enumerate(duplicate_children):
                result = self.reply_regex.search(third_child.content)
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
        reply_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[5]/div/div[{j}]/div/div[2]/div[1]/div/a'
        reply_name_elem = self.driver.find_element(By.XPATH, reply_name_xpath)

        reply_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[5]/div/div[{j}]/div/div[2]/div[2]'
        reply_content_elem = self.driver.find_element(By.XPATH, reply_content_xpath)

        self.driver.implicitly_wait(1)

        node = ReplyNode(username=reply_name_elem.text, content=reply_content_elem.text)
        root.add(node)

        return root

    @staticmethod
    def show_more(comment_elem):
        try:
            while True:
                show_more_elem = comment_elem.find_element(By.CLASS_NAME, 'show-more')
                if show_more_elem is None:
                    break
                show_more_elem.click()
                # scroll(self.driver, count=10, offset=6000)
                time.sleep(random.uniform(3, 6))
        except NoSuchElementException:
            pass

    def __collect(self, root: ReplyNode, max_post_count=20, max_response_count=100):

        # Show more comments
        for i in range(1, max_post_count):
            comment_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[{i}]'
            comment_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[2]'
            comment_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[{i}]/div/div[2]/div[1]/div/a'

            comment_name_elem = self.driver.find_element(By.XPATH, comment_name_xpath)
            comment_elem = self.driver.find_element(By.XPATH, comment_xpath)
            comment_content_elem = self.driver.find_element(By.XPATH, comment_content_xpath)
            self.driver.implicitly_wait(1)

            username = comment_name_elem.text
            content = comment_content_elem.text

            if username == '' or content == '':
                continue

            comment = ReplyNode(username, content)
            root.add(comment)

            self.show_more(comment_elem)

            # Deep Search

            for j in range(1, max_response_count):
                comment = self.__deep(comment, i, j)

            xhs_scroll(self.driver, 1, random.uniform(3, 6))

        return root

    def collect(self, post_id: str):
        open_page(self.driver, f'https://www.xiaohongshu.com/explore/{post_id}')

        # Start collect
        logging.debug(f'🗨️ Collecting replies from the page. ')

        # Just get root node without children
        root = self.__get_root()

        # Refactored root with children
        root = self.__collect(root)

        self.__refactor(root)

        # At filter to remove atmark
        root = at_filter(root)

        return root
