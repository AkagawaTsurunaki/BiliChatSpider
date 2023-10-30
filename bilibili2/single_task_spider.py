import logging

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.common import open_page, scroll, find_element
from core.data_structure import ReplyNode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SingleTaskSpider:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def __get_root(self):
        title_elem_xpath = f'/html/body/div[2]/div[2]/div[1]/div[1]/h1'
        detail_elem_xpath = f'/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div[1]'
        username_elem_xpath = f'/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/a[1]'

        title_elem = find_element(self.driver, By.XPATH, title_elem_xpath, 2, 0, False)
        username_elem = find_element(self.driver, By.XPATH, username_elem_xpath, 2, 0, False)
        detail_elem = find_element(self.driver, By.XPATH, detail_elem_xpath, 2, 0, True)

        assert title_elem is not None
        assert username_elem is not None

        content = title_elem.text
        content += '\n'
        content += detail_elem.text if detail_elem is not None else ''

        return ReplyNode(content=content, username=username_elem.text)

    def __show_more_next_page(self, container: WebElement):
        try:
            pagination_btn = container.find_element(By.CLASS_NAME, 'pagination-btn')
            self.driver.implicitly_wait(1)
            pagination_btn.click()
        except NoSuchElementException:
            pass

    def __show_more(self, container: WebElement):
        try:
            view_more_btn = container.find_element(By.CLASS_NAME, 'view-more-btn')
            self.driver.implicitly_wait(1)
            view_more_btn.click()
        except NoSuchElementException:
            pass

    def __deep(self, node: ReplyNode, i, j):
        reply_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(3) > div:nth-child(1) > div:nth-child({j}) > span:nth-child(2) > span:nth-child(1)'
        username_elem_xpath = f'/html/body/div[2]/div[2]/div[1]/div[4]/div[3]/div/div/div/div[2]/div[2]/div[{i}]/div[3]/div/div[{j}]/div[1]/div[2]'

        reply_elem, _ = find_element(self.driver, By.CSS_SELECTOR, reply_elem_css, 2, 0, False)
        username_elem, _ = find_element(self.driver, By.XPATH, username_elem_xpath, 2, 0, False)

        assert reply_elem is not None
        assert username_elem is not None

        node.add(ReplyNode(content=reply_elem.text, username=username_elem.text))

    def collect(self, bv):
        open_page(driver=self.driver, url=f"https://www.bilibili.com/video/{bv}")
        scroll(driver=self.driver, offset=6000, count=10, sleep_time=0.7)
        root = self.__get_root()
        try:
            for i in range(1, 1000):
                comment_container_xpath = f'/html/body/div[2]/div[2]/div[1]/div[4]/div[3]/div/div/div/div[2]/div[2]/div[{i}]'
                comment_elem_css = f'div.reply-item:nth-child({i}) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)'
                username_elem_xpath = f'/html/body/div[2]/div[2]/div[1]/div[4]/div[3]/div/div/div/div[2]/div[2]/div[{i}]/div[2]/div[2]/div[2]/div'

                comment_container, _ = find_element(self.driver, By.XPATH, comment_container_xpath, 2, 0, False)
                comment_elem, _ = find_element(self.driver, By.CSS_SELECTOR, comment_elem_css, 2, 0, False)
                username_elem, _ = find_element(self.driver, By.XPATH, username_elem_xpath, 2, 0, False)

                assert comment_container is not None
                assert comment_elem is not None
                assert username_elem is not None

                node = ReplyNode(content=comment_elem.text, username=username_elem.text)
                root.add(node)

                self.__show_more(comment_container)

                try:
                    self.__show_more(comment_container)
                    for j in range(1, 50):
                        for k in range(1, 20):
                            self.__deep(node, i, k)
                        self.__show_more_next_page(comment_container)
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            pass
