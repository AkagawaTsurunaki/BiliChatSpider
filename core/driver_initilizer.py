import logging
from retry import retry
from selenium import webdriver

from config import chat_spider_config as cfg


class DriverInitializer:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    @retry(Exception, tries=2)
    def get_firefox_driver(image: bool = False, stylesheet: bool = False):
        # User data path
        firefox_profile_dir = cfg.firefox_profile_dir
        # Init webdriver option
        profile = webdriver.FirefoxProfile(firefox_profile_dir)
        options = webdriver.FirefoxOptions()
        # Image permission
        if not image:
            options.set_preference('permissions.default.image', 2)
            logging.debug(f'permissions.default.image is set to 2, images in the website will not be loaded.')
        # Stylesheet permission
        if not stylesheet:
            options.set_preference('permissions.default.stylesheet', 2)
            logging.debug(f'permissions.default.stylesheet is set to 2, css in the website will not be loaded.')

        options.profile = profile
        driver = webdriver.Firefox(options=options)

        return driver
