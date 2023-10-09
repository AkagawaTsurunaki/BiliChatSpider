import logging
import random
import time

from selenium.webdriver.common.by import By


class SingleTaskSpider:
    @staticmethod
    def __is_bv_valid(bv: str) -> bool:
        if bv == '' or bv is None:
            return False
        if len(bv) != 12:
            return False
        if bv[:2] != 'BV':
            return False
        return True

    def __init__(self, driver):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.reply_record_list = []
        self.driver = driver
        self.implicitly_wait_second = 0.5
        self.window_scroll_count = 10
        self.window_scroll_by = 6000

    def get_reply_records(self, bv: str):
        """
        Get reply list from specified video.
        """
        # If bv is valid
        if self.__is_bv_valid(bv):

            # Open specified page
            url = f"https://www.bilibili.com/video/{bv}"
            self.driver.get(url)

            # Wait for loading of resources
            self.driver.implicitly_wait(5)
            time.sleep(random.Random().random() * 5)
            logging.debug(f'🌐 Successfully open the page at {url}". ')

            # Control the page to scroll
            for _ in range(self.window_scroll_count):
                time.sleep(0.7)
                self.driver.execute_script(f'window.scrollBy(0,{self.window_scroll_by})')
            logging.debug(
                f'🖱️ Total number of pixels of scrolling is {self.window_scroll_count * self.window_scroll_by}. ')

            # Start collect
            logging.debug(f'🗨️ Collecting replies from the page. ')

            self.__get_reply_records()

            return self.__unblank(self.__unique(self.reply_record_list))

        else:
            raise ValueError(f'❌ Invalid bv = {bv}. ')

    def __get_reply_records(self):
        no_such_element_exception_raise = 0
        for i in range(1, 60):
            reply_content_elems = self.driver.find_elements(By.CSS_SELECTOR,
                                                            f'div.reply-item:nth-child({i}) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)')
            self.driver.implicitly_wait(2)
            # 1 <= k <= 3
            if len(reply_content_elems) != 0:

                for j in range(1, 3 + 1):
                    subreply_content_elems = self.driver.find_elements(By.CSS_SELECTOR,
                                                                       f'div.reply-item:nth-child({i}) > div:nth-child(3) > div:nth-child(1) > div:nth-child({j}) > span:nth-child(2) > span:nth-child(1)')
                    if len(subreply_content_elems) != 0:
                        record = {
                            "post": reply_content_elems[0].text,
                            "response": subreply_content_elems[0].text
                        }
                        self.reply_record_list.append(record)
                        no_such_element_exception_raise //= 2
                    else:
                        no_such_element_exception_raise += 1
            else:
                no_such_element_exception_raise += 1

            if no_such_element_exception_raise >= 39:
                return

    @staticmethod
    def __unique(origin_list: list):
        unique_list = []
        for item in origin_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list

    @staticmethod
    def __unblank(origin_list: list):
        filtered_list = []
        for item in origin_list:
            if item["post"] != '' and item["response"] != '':
                filtered_list.append(item)
        return filtered_list
