from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

CHROME_DRIVER_PATH = 'c://webdrivers/chromedriver.exe'


class Spider:
    name = None
    driver = None

    def execute(self, *args, **kwargs):
        try:
            self.init_driver(*args, **kwargs)
            self.pre_process_data()
            for data in self.parse(*args, **kwargs):
                self.process_data(data)

        finally:
            self.post_process_data()
            self.destroy_driver()

    def init_driver(self, *args, **kwargs):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        return self.driver

    def destroy_driver(self):
        if self.driver:
            self.driver.close()

    def parse(self, *args, **kwargs):
        print('NOT IMPLEMENTED')
        return ()

    def process_data(self, data):
        print(data)

    def pre_process_data(self):
        pass

    def post_process_data(self):
        pass


