import json
import logging
import random
import re
import time

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
        detail_xpath = '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[1]/div[2]/span[1]'

        # detail_xpath = '//*[@id="detail-desc"]'

        username_elem, e = find_element(self.driver, By.XPATH, username_xpath, 2, 0, False)
        title_elem, e = find_element(self.driver, By.XPATH, title_xpath, 2, 0, True)
        detail_elem, e = find_element(self.driver, By.XPATH, detail_xpath, 2, 0, True)

        username_txt = username_elem.text
        title_elem_txt = title_elem.text if title_elem is not None else ''
        detail_elem_txt = detail_elem.text if detail_elem is not None else ''

        if len(title_elem_txt) == 0 and len(detail_elem_txt) == 0:
            raise NoSuchElementException('Title and Detail must be non-null at least,')

        content_txt = title_elem_txt + '\n' + detail_elem_txt

        root = ReplyNode(username_txt, content_txt)

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

        reply_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[3]/div/div[2]/div[{i}]/div[2]/div/div[{j}]/div/div[2]/div[1]/div/a'
        reply_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[3]/div/div[2]/div[{i}]/div[2]/div/div[{j}]/div/div[2]/div[2]'

        reply_name_elem, _ = find_element(self.driver, By.XPATH, reply_name_xpath, 2, 0, False)
        reply_content_elem, _ = find_element(self.driver, By.XPATH, reply_content_xpath, 2, 0, True)

        node = ReplyNode(username=reply_name_elem.text, content=reply_content_elem.text)
        root.add(node)

        return root

    def __show_more(self, comment_elem):
        try:
            while True:
                show_more_elem = comment_elem.find_element(By.CLASS_NAME, 'show-more')
                self.driver.implicitly_wait(2)
                if show_more_elem is None:
                    break
                show_more_elem.click()
                time.sleep(random.uniform(0.5, 1.5))
        except NoSuchElementException:
            pass

    def __collect(self, root: ReplyNode, max_post_count=100, max_response_count=1000):
        try:
            # Show more comments
            for i in range(1, max_post_count):
                comment_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[3]/div/div[2]/div[{i}]'
                comment_name_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[3]/div/div[2]/div[{i}]/div[1]/div/div[2]/div[1]/div/a'
                comment_content_xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div[3]/div/div[2]/div[{i}]/div[1]/div/div[2]/div[2]'

                comment_elem, _ = find_element(self.driver, By.XPATH, comment_xpath, 2, 0, False)
                comment_name_elem, _ = find_element(self.driver, By.XPATH, comment_name_xpath, 2, 0, False)
                comment_content_elem, _ = find_element(self.driver, By.XPATH, comment_content_xpath, 2, 0, False)

                username = comment_name_elem.text
                content = comment_content_elem.text

                comment_node = ReplyNode(username, content)
                root.add(comment_node)

                self.__show_more(comment_elem)

                # Deep Search

                try:
                    for j in range(1, max_response_count):
                        comment_node = self.__deep(comment_node, i, j)
                except NoSuchElementException:
                    pass

                xhs_scroll(self.driver, 1, random.uniform(0.5, 1.5))
        except NoSuchElementException:
            pass

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
