from paths import *
import logging
from selenium.common.exceptions import NoSuchElementException
from functions import *
from urls import *


def idxs_testmethod(s, driver):
    data = call_url_post(mdata_url, mdata_idxs_body)
    filtered = mdata_resp_filtration(data)
    prices = idxs_prices(filtered)
    wait_till_find_id(driver, idxs_carousel)

    try:
        s.assertIsNotNone(driver.find_element_by_android_uiautomator(
            'new UiSelector().className("android.widget.TextView").text('
            f'"RTS")'))

        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                               '"android.view.ViewGroup").descriptionStartsWith( '
                                                           f'"RTS")')
        price = find_index_price(card)
        s.assertEqual(price.text, prices[0]['price'])
    except AssertionError:
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"RTS")')
        price = find_index_price(card)
        logging.error(f"Index RTS, Actual price: {price.text}, Expected price : {prices[0]['price']}")
    except NoSuchElementException:
        logging.error("Index RTS not found")

    try:
        s.assertIsNotNone(driver.find_element_by_android_uiautomator(
            'new UiSelector().className("android.widget.TextView").text('
            f'"IMOEX")'))
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"IMOEX")')
        price = find_index_price(card)
        s.assertEqual(price.text, prices[1]['price'])
    except AssertionError:
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"IMOEX")')
        price = find_index_price(card)
        logging.error(f"Index IMOEX, Actual price: {price.text}, Expected price : {prices[1]['price']}")
    except NoSuchElementException:
        logging.error("Index IMOEX not found")

    try:
        s.assertIsNotNone(driver.find_element_by_android_uiautomator(
            'new UiSelector().className("android.widget.TextView").text('
            f'"EUR")'))
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"EUR")')
        price = find_index_price(card)
        s.assertEqual(price.text, prices[2]['price'])
    except AssertionError:
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"EUR")')
        price = find_index_price(card)
        logging.error(f"Index EUR, Actual price: {price.text}, Expected price : {prices[2]['price']}")
    except NoSuchElementException:
        logging.error("Index EUR not found")

    driver.swipe(974, 987, 126, 987)
    try:
        s.assertIsNotNone(driver.find_element_by_android_uiautomator(
            'new UiSelector().className("android.widget.TextView").text('
            '"USD")'))
        card = driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                          '"android.view.ViewGroup").descriptionStartsWith( '
                                                          '"USD")')
        price = find_index_price(card)
        s.assertEqual(price.text, prices[3]['price'])
    except AssertionError:
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"USD")')
        price = find_index_price(card)
        logging.error(f"Index USD, Actual price: {price.text}, Expected price : {prices[3]['price']}")
    except NoSuchElementException:
        logging.error("Index USD not found")

    try:
        s.assertIsNotNone(driver.find_element_by_android_uiautomator(
            'new UiSelector().className("android.widget.TextView").text('
            '"Нефть")'))
        card = driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                          '"android.view.ViewGroup").descriptionStartsWith('
                                                          '"Нефть")')
        price = find_index_price(card)
        s.assertEqual(price.text, prices[4]['price'])
    except AssertionError:
        card = s.driver.find_element_by_android_uiautomator('new UiSelector().className('
                                                            '"android.view.ViewGroup").descriptionStartsWith( '
                                                            f'"Нефть")')
        price = find_index_price(card)
        logging.error(f"Index Нефть, Actual price: {price.text}, Expected price : {prices[4]['price']}")
    except NoSuchElementException:
        logging.error("Index Нефть not found")
