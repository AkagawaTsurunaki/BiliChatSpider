from retry import retry
from selenium import webdriver

from config import chat_spider_config as cfg


class DriverInitializer:
    @staticmethod
    @retry(Exception, tries=2)
    def get_firefox_driver():
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
