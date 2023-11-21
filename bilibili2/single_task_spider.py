import logging
import re
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.common import open_page, scroll, find_element
from core.data_structure import ReplyNode
from data_clean.filter.at_filter import at_filter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SingleTaskSpider:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.reply_regex = re.compile('回复\s*@\s*(.*)\s*[：:]\s*(.*)')

    def __get_root(self):
        title_elem_xpath = f'.video-title'
        detail_elem_xpath = f'.basic-desc-info'
        username_elem_xpath = f'html body.harmony-font.header-v3.win div#app.app-v1 div#mirror-vdcon.video-container-v1 div.right-container.is-in-large-ab div.right-container-inner.scroll-sticky div.up-panel-container div.up-info-container div.up-info--right div.up-info__detail div.up-detail div.up-detail-top a.up-name'

        title_elem, _ = find_element(self.driver, By.CSS_SELECTOR, title_elem_xpath, 2, 0, False)
        username_elem, _ = find_element(self.driver, By.CSS_SELECTOR, username_elem_xpath, 2, 0, False)
        detail_elem, _ = find_element(self.driver, By.CSS_SELECTOR, detail_elem_xpath, 2, 0, True)

        assert title_elem is not None
        assert username_elem is not None

        content = title_elem.text
        content += '\n'
        content += detail_elem.text if detail_elem is not None else ''

        return ReplyNode(content=content, username=username_elem.text)

    def __show_more_next_page(self, container: WebElement, sleep_time=1):
        pagination_btns = container.find_elements(By.CLASS_NAME, 'pagination-btn')
        self.driver.implicitly_wait(5)
        for pagination_btn in pagination_btns:
            if pagination_btn.text == '下一页':
                time.sleep(sleep_time)
                self.driver.execute_script('arguments[0].click()', pagination_btn)
                return True
        return False

    def __show_more(self, container: WebElement, sleep_time=1):
        try:
            time.sleep(sleep_time)
            view_more_btn = container.find_element(By.CLASS_NAME, 'view-more-btn')
            self.driver.implicitly_wait(3)
            self.driver.execute_script('arguments[0].click()', view_more_btn)
        except Exception:
            pass

    def __deep(self, node: ReplyNode, i, j):
        reply_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(3) > div:nth-child(1) > div:nth-child({j}) > span:nth-child(2) > span:nth-child(1)'
        username_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(3) > div:nth-child(1) > div:nth-child({j}) > div:nth-child(1) > div:nth-child(2)'

        reply_elem, _ = find_element(self.driver, By.CSS_SELECTOR, reply_elem_css, 2, 0, False)
        username_elem, _ = find_element(self.driver, By.CSS_SELECTOR, username_elem_css, 2, 0, False)

        node.add(ReplyNode(content=reply_elem.text, username=username_elem.text))

    def collect(self, bv, comment_count=100, page_per_comment=50, reply_count=20):
        open_page(driver=self.driver, url=f"https://www.bilibili.com/video/{bv}")
        scroll(driver=self.driver, offset=2000, count=1, sleep_time=0.7)
        time.sleep(3)
        root = self.__get_root()
        try:
            for i in range(1, comment_count):

                comment_container_xpath = f'div.reply-item:nth-child({i})'
                comment_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)'
                username_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)'

                comment_container, _ = find_element(self.driver, By.CSS_SELECTOR, comment_container_xpath, 2, 0, False)
                comment_elem, _ = find_element(self.driver, By.CSS_SELECTOR, comment_elem_css, 2, 0, False)
                username_elem, _ = find_element(self.driver, By.CSS_SELECTOR, username_elem_css, 2, 0, False)

                assert comment_container is not None
                assert comment_elem is not None
                assert username_elem is not None

                node = ReplyNode(content=comment_elem.text, username=username_elem.text)
                root.add(node)
                self.__show_more(comment_container, sleep_time=2)

                try:
                    # j means page
                    for page in range(1, page_per_comment):
                        try:
                            for k in range(1, reply_count):
                                self.__deep(node, i, k)
                        except Exception:
                            pass
                        if not self.__show_more_next_page(comment_container):
                            break
                except NoSuchElementException:
                    pass

                scroll(driver=self.driver, offset=1500, count=1, sleep_time=0.7)

        except NoSuchElementException as e:
            pass
        self.__refactor(root)
        root = at_filter(root)
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
                reply_to = result.groups()[0].split(' ')[0]
                third_child.content = result.groups()[1]

                appended = False
                for recent_child in duplicate_children[i::-1]:
                    if recent_child.username == reply_to:
                        recent_child.children.append(third_child)
                        appended = True
                        break
                if not appended:
                    second_child.children.append(third_child)
