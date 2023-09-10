import logging
from multiprocessing import Process

from retry import retry
from selenium import webdriver

from config import chat_spider_config as cfg
from core.single_task_spider import SingleTaskSpider
from dataset_manager import DatasetManager
from history import History


class MultitaskSpider:

    def __init__(self, up_name: str, uid: str):
        self.up_name = up_name
        self.uid = uid
        self.job = []

    @staticmethod
    @retry(Exception, tries=2)
    def __get_driver():
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

    @staticmethod
    def __run_single_task(history: History, uid: str, bv: str):
        logging.debug(f'Task {bv} executing...')
        driver = MultitaskSpider.__get_driver()
        data = SingleTaskSpider(driver).get_reply_records(bv)
        DatasetManager().save_single_task(uid=uid, bv=bv, data=data)
        history.single_task_completed(uid=uid, bv=bv)
        driver.close()
        driver.quit()
        logging.debug(f'Task {bv} completed.')

    def run(self):

        # If the job is completed then return straightly
        history = History()
        if history.is_job_completed(self.uid):
            return

        # If the job is not completed,
        # Get the uncompleted bv list.
        processes = []
        for bv in history.get_uncompleted_tasks(self.uid):
            process = Process(target=MultitaskSpider.__run_single_task, args=(history, self.uid, bv))
            processes.append(process)

        # Start all processes.
        for process in processes:
            process.start()

        # Waiting for all processes completed.
        for process in processes:
            process.join()
