import unittest
from card_details import *
from MarketTest import MarketTest
from urls import *
from idxs import *
from card_details_currency import *
from card_detail_bonds import *
from review_company_data import *


class TestCardDet(MarketTest):

    def test_1idxs_prices(self):
        self.driver.find_element_by_accessibility_id("Рынок").click()
        idxs_testmethod(s=self, driver=self.driver)

    def test_card_param_1stock(self):
        wait_till_find_xpath(self.driver, stocks_btn).click()
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name, mdata_body=mdata_req_body1)
        card_companydataview(s=self, driver=self.driver, name=name, gql_body=gql_st_body_1)

    def test_card_param_2stock(self):
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name1, mdata_body=mdata_req_body2)

    def test_card_param_3stock(self):
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name2, mdata_body=mdata_req_body3)

    def test_card_param_3vcurrency(self):
        wait_till_find_xpath(self.driver, backward_btn)
        find_by_xpath(self.driver, backward_btn).click()
        wait_till_find_xpath(self.driver, currency_btn)
        find_by_xpath(self.driver, currency_btn).click()
        wait_till_find_xpath(self.driver, eur_card)
        card_details_currency_testmethod(s=self, driver=self.driver, name=name6, mdata_body=mdata_req_body7)

    def test_card_param_4fund(self):
        wait_till_find_xpath(self.driver, backward_btn)
        find_by_xpath(self.driver, backward_btn).click()
        wait_till_find_xpath(self.driver, funds_btn)
        find_by_xpath(self.driver, funds_btn).click()
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name3, mdata_body=mdata_req_body4)
        card_companydataview(s=self, driver=self.driver, name=name3, gql_body=gql_fd_body_1)

    def test_card_param_5fund(self):
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name4, mdata_body=mdata_req_body5)

    def test_card_param_6fund(self):
        wait_till_find_xpath(self.driver, card_name)
        card_details_testmethod(s=self, driver=self.driver, name=name5, mdata_body=mdata_req_body6)

    def test_card_param_7bond(self):
        wait_till_find_xpath(self.driver, backward_btn)
        find_by_xpath(self.driver, backward_btn).click()
        wait_till_find_xpath(self.driver, bonds_btn).click()
        wait_till_find_xpath(self.driver, card_name)
        card_details_bond_testmethod(s=self, driver=self.driver, name=name7, mdata_body=mdata_req_body8, graphQlbody=gql_bond_body1)
        card_companydataview(s=self, driver=self.driver, name=name7, gql_body=gql_bond_body1)

    def test_card_param_8bond(self):
        wait_till_find_xpath(self.driver, card_name)
        card_details_bond_testmethod(s=self, driver=self.driver, name=name8, mdata_body=mdata_req_body9, graphQlbody=gql_bond_body2)











