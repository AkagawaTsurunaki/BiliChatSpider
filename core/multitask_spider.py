import logging
import random
import time
import traceback

from retry import retry
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from config import chat_spider_config as cfg
from core.single_task_spider import SingleTaskSpider
from dataset_manager import DatasetManager


class MultitaskSpider:

    def __init__(self, up_name: str, uid: str):
        self.up_name = up_name
        self.uid = uid
        self.driver = self.__init_firefox_driver()
        self.bili_spider = SingleTaskSpider(self.driver)

    def __init_firefox_driver(self):
        # 用户数据路径
        firefox_profile_dir = cfg.firefox_profile_dir
        # 实例化火狐设置选项
        profile = webdriver.FirefoxProfile(firefox_profile_dir)
        options = webdriver.FirefoxOptions()
        # 禁用加载图片
        options.set_preference('permissions.default.image', 2)
        # 禁用CSS
        options.set_preference('permissions.default.stylesheet', 2)

        options.profile = profile
        driver = webdriver.Firefox(options=options)

        return driver

    def __run(self):

        diff_set = self.get_unsaved_video_list()

        for bv in diff_set:
            reply_content_list = self.bili_spider.get_reply_records(bv)
            DatasetManager.save_task(up_name=self.up_name, bv=bv, uid=self.uid, data=reply_content_list)

        self.driver.close()

    # def get_unsaved_video_list(self):
    #     video_list = self.get_video_list()
    #     saved_video_list = self.dataset_manager.get_saved_video_list_by_space_id(self.uid)
    #     diff_set = set(video_list) - set(saved_video_list)
    #     return diff_set

    @retry(NoSuchElementException, tries=2)
    def get_video_list(self):
        video_list = []
        page_num = 1
        while True:
            url = f'https://space.bilibili.com/{self.uid}/video?tid=0&pn={page_num}&keyword=&order=pubdate'
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            # 减速, 防止触发验证码
            time.sleep(random.Random().randint(a=1, b=2))
            elems = self.driver.find_element(By.CLASS_NAME, 'list-list').find_elements(By.CLASS_NAME, 'list-item')
            self.driver.implicitly_wait(20)
            if len(elems) == 0: break
            for elem in elems:
                bv = elem.get_attribute('data-aid')
                video_list.append(bv)
            page_num += 1
        self.driver.close()

        return video_list

    @retry(Exception, delay=4, tries=2)
    def run_single(self, bv: str):

        logging.debug(f'开始抓取“{bv}”的评论区评论区……')
        reply_content_list = self.bili_spider.get_reply_records(bv)

        self.dataset_manager.save(bv, self.uid, reply_content_list)
        self.driver.close()
        self.driver.quit()

    def run(self):
        try:
            logging.debug(f'蜘蛛大军即将启动。')
            self.__run()
            logging.debug('蜘蛛大军席卷完毕！')
        except Exception as e:
            traceback.print_exc()
            logging.fatal('❌ 蜘蛛大军退出，因为遇到了未经处理的异常。')
        finally:
            self.driver.close()
            self.driver.quit()
