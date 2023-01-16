from paths import *
from urls import mdata_url
import logging
from selenium.common.exceptions import NoSuchElementException
from functions import *


def card_details_testmethod(s, driver, name, mdata_body):
    try:
        driver.find_element_by_android_uiautomator(
            f'new UiSelector().className("android.widget.TextView").resourceId('
            f'"ru.sberbank.investor.dev:id/title").text("{name}")').click()
        resp = call_url_post(mdata_url, mdata_body)['resp']['data'][0]
        try:
            wait_till_find_id(driver, card_title)
            s.assertEqual(find_by_id(driver, bid_text).text, "Продажа")
            s.assertEqual(find_by_id(driver, offer_text).text, "Покупка")
            s.assertEqual(find_by_id(driver, card_ticker).text, resp['key']['ticker'])
        except NoSuchElementException:
            logging.error("Ну что ж")

        try:
            s.assertEqual(find_by_id(driver, card_price).text,
                          prices_formatting(resp["value"]["lastPrice"]))
            s.assertEqual(find_by_id(driver, card_bid).text, prices_formatting(resp["value"]["bid"]))
            s.assertEqual(find_by_id(driver, card_offer).text,
                          prices_formatting(resp["value"]["offer"]))
        except NoSuchElementException:
            logging.error('Bid / offer element not found')
        except AssertionError:
            logging.error(
                f'Actual: {find_by_id(driver, card_ticker).text}, {find_by_id(driver, card_price).text}, {find_by_id(driver, card_bid).text}, {find_by_id(driver, card_offer).text}. Expected: {resp["key"]["ticker"]}, {prices_formatting(resp["value"]["lastPrice"])}, {prices_formatting(resp["value"]["bid"])}, {prices_formatting(resp["value"]["offer"])}')
        try:
            s.assertEqual(driver.find_element(By.ID, login_btn).text, "Войти")
        except NoSuchElementException:
            logging.error('Button element not found')
        if resp['value']['tradingStatus'] == 'TRADING_AVAILABLE':
            try:
                s.assertEqual(driver.find_element(By.ID, card_abs).text,
                              formatting_abs_price_change(absolute_value(resp['value'])))
            except AssertionError:
                logging.error(
                    f"Actual result: {driver.find_element(By.ID, card_abs).text}, Expected result: {formatting_abs_price_change(absolute_value(resp['value']))}")
            except NoSuchElementException:
                logging.error('Abs not found')
            try:
                s.assertEqual(driver.find_element(By.ID, card_ref).text,
                              formatting_ref_price_change(refer_change_value(resp['value'])))
            except AssertionError:
                logging.error(
                    f"Actual result: {driver.find_element(By.ID, card_ref).text}, Expected result: {formatting_ref_price_change(refer_change_value(resp['value']))}")
            except NoSuchElementException:
                logging.error('Ref not found')
        else:
            pass

        driver.swipe(500, 1838, 500, 700)
        try:
            card = find_by_id(driver, open_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
                s.assertEqual(text.text, "Цена открытия")
                s.assertEqual(price.text, prices_formatting(resp['value']['open']))
            except AssertionError:
                logging.error(
                    f"Actual: {text.text}, {price.text}, Expected: 'Цена открытия', {prices_formatting(resp['value']['open'])}")
        except NoSuchElementException:
            logging.error(
                "Open price statistics not found")
        try:
            card = find_by_id(driver, close_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
                s.assertEqual(text.text, "Цена закрытия")
                s.assertEqual(price.text, prices_formatting(resp['value']['closePrice']))
            except AssertionError:
                logging.error(
                    f"Actual: {text.text}, {price.text}, Expected: 'Цена закрытия', {prices_formatting(resp['value']['closePrice'])}")
        except NoSuchElementException:
            logging.error(
                "Close price statistics not found")
        try:
            card = find_by_id(driver, range_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
               s.assertEqual(text.text, "Дневной диапазон")
               s.assertEqual(price.text,
                          f"{prices_formatting(resp['value']['lowAsk'])} - {prices_formatting(resp['value']['highBid'])}")
            except AssertionError:
               logging.error(
                f"Actual: {text.text}, {price.text}, Expected: 'Дневной диапазон', f'{prices_formatting(resp['value']['lowAsk'])} - {prices_formatting(resp['value']['highBid'])}' ")
        except NoSuchElementException:
            logging.error("Daily range not found")
        driver.find_element_by_accessibility_id('Вернуться назад').click()
    except ConnectionError:
        driver.find_element_by_accessibility_id('Вернуться назад').click()
