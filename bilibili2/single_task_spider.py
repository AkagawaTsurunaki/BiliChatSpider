import logging

from selenium.webdriver.firefox.webdriver import WebDriver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class SingleTaskSpider:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def collect(self, bv):
        pass