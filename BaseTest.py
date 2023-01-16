from unittest import TestCase
from appium import webdriver


class AppiumTest(TestCase):
    dc = {}
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.dc['app'] = 'd:\\ru.sberbank.investor.dev_1.19.0-26.apk'
        cls.dc['appPackage'] = 'ru.sberbank.investor.dev'

        cls.dc['platformName'] = 'Android'
        cls.dc['deviceName'] = 'Pixel 5'
        cls.dc['udid'] = 'emulator-5554'

        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", cls.dc)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
