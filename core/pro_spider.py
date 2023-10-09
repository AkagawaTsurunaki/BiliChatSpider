import time
from random import Random

from retry import retry
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from core.history_manager import HistoryManager
from core.driver_initilizer import DriverInitializer


class ProSpider:

    def __init__(self):
        self.driver = DriverInitializer.get_firefox_driver()

    def update_job(self, uid: str, force_create_job: bool = False):

        if HistoryManager.is_job_completed(uid=uid) is None or force_create_job:
            up_name, uncompleted_tasks = self.get_video_list(uid=uid)
            HistoryManager.create_job(up_name=up_name, uid=uid, uncompleted_tasks=uncompleted_tasks)

    @retry(NoSuchElementException, tries=2)
    def get_video_list(self, uid: str, implicitly_wait_time: int = 20):
        video_list = []
        page_num = 1

        self.driver.get(f'https://space.bilibili.com/{uid}')
        self.driver.implicitly_wait(implicitly_wait_time)
        up_name = self.driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/span[1]').text

        while True:
            # Open specified page.
            url = f'https://space.bilibili.com/{uid}/video?tid=0&pn={page_num}&keyword=&order=pubdate'
            self.driver.get(url)
            self.driver.implicitly_wait(implicitly_wait_time)

            # Slow down the page switching to prevent triggering the captcha.
            time.sleep(Random().randint(a=1, b=3))

            # Find elements that contain information of the video list.
            elems = self.driver.find_element(By.CLASS_NAME, 'list-list').find_elements(By.CLASS_NAME, 'list-item')
            self.driver.implicitly_wait(implicitly_wait_time)
            time.sleep(Random().randint(a=3, b=5))

            # If there are no more specified elements to be found, then break.
            if len(elems) == 0:
                break

            # Convert to a video list as Python list.
            for elem in elems:
                bv = elem.get_attribute('data-aid')
                video_list.append(bv)

            # Switch to the next page.
            page_num += 1

        # Close the driver to release resources.
        self.driver.close()

        return up_name, video_list
