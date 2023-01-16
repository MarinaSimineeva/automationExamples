from BaseTest import AppiumTest
from paths import promo_tab_forward, market_tab
from functions import find_by_id, find_by_xpath, wait_till_find_xpath, find_clickable_xpath, wait_till_find_id


class MarketTest(AppiumTest):
    @classmethod
    def setUpClass(cls):
        super(MarketTest, cls).setUpClass()
        wait_till_find_xpath(cls.driver, promo_tab_forward)
        find_by_xpath(cls.driver, promo_tab_forward).click()
        find_clickable_xpath(promo_tab_forward)
        find_by_xpath(cls.driver, promo_tab_forward).click()
        find_clickable_xpath(promo_tab_forward)
        find_by_xpath(cls.driver, promo_tab_forward).click()
        wait_till_find_id(cls.driver, market_tab)
        #find_by_id(cls.driver, market_tab)

