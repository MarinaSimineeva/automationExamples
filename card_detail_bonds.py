from paths import *
from urls import mdata_url, graphQl_url
import logging
from selenium.common.exceptions import NoSuchElementException
from functions import *


def card_details_bond_testmethod(s, driver, name, mdata_body, graphQlbody):
    try:
        driver.find_element_by_android_uiautomator(
            f'new UiSelector().className("android.widget.TextView").resourceId('
            f'"ru.sberbank.investor.dev:id/title").text("{name}")').click()
        resp = call_url_post(mdata_url, mdata_body)['resp']['data'][0]
        gql_resp = call_url_post(graphQl_url, graphQlbody)
        try:
            wait_till_find_id(driver, card_title)
            s.assertEqual(find_by_id(driver, bid_text).text, "Продажа")
            s.assertEqual(find_by_id(driver, offer_text).text, "Покупка")
            s.assertEqual(find_by_id(driver, card_ticker).text, resp['key']['ticker'])
        except NoSuchElementException:
            logging.error("Ну что ж")

        try:
            s.assertEqual(find_by_id(driver, card_price).text,
                          prices_formatting(last_price_bond_counter(resp)))
            s.assertEqual(find_by_id(driver, card_bid).text, prices_formatting(bid_bond_counter(resp)))
            s.assertEqual(find_by_id(driver, card_offer).text,
                          prices_formatting(offer_bond_counter(resp)))
        except NoSuchElementException:
            logging.error('Bid / offer element not found')
        except AssertionError:
            logging.error(
                f'Actual: {find_by_id(driver, card_ticker).text}, {find_by_id(driver, card_price).text}, {find_by_id(driver, card_bid).text}, {find_by_id(driver, card_offer).text}. Expected: {resp["key"]["ticker"]}, {prices_formatting(last_price_bond_counter(resp))}, {prices_formatting(bid_bond_counter(resp))}, {prices_formatting(offer_bond_counter(resp))}')
        try:
            s.assertEqual(driver.find_element(By.ID, login_btn).text, "Войти")
        except NoSuchElementException:
            logging.error('Button element not found')
        if resp['value']['tradingStatus'] == 'TRADING_AVAILABLE':
            try:
                s.assertEqual(driver.find_element(By.ID, card_abs).text,
                              formatting_abs_price_change(absolute_bond_value(resp)))
            except AssertionError:
                logging.error(
                    f"Actual result: {driver.find_element(By.ID, card_abs).text}, Expected result: {formatting_abs_price_change(absolute_bond_value(resp))}")
            except NoSuchElementException:
                logging.error("absolute price change not found")
            try:
                s.assertEqual(driver.find_element(By.ID, card_ref).text,
                              formatting_ref_price_change(ref_bond_value(resp)))
            except AssertionError:
                logging.error(
                    f"Actual result: {driver.find_element(By.ID, card_ref).text}, Expected result: {formatting_ref_price_change(ref_bond_value(resp))}")
            except NoSuchElementException:
                logging.error("percent price change not found")
        else:
            pass
        driver.swipe(500, 1838, 500, 700)

        if resp['value']['bondData']['yieldPcnt'] not in [0, None]:
            try:
                card = find_by_id(driver, maturityYield)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, formatting_ref_price_change(resp['value']['bondData']['yieldPcnt']))
                    s.assertEqual(text.text, "Доходность")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Доходность', {formatting_ref_price_change(resp['value']['bondData']['yieldPcnt'])}")
            except NoSuchElementException:
                logging.error("maturityYield not found")
        else:
            pass

        if gql_resp['data']['instruments'][0]['bondParams']['maturityDate'] not in [0, None]:
            try:
                card = find_by_id(driver, maturityDate)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, str(formatting_dates(gql_resp['data']['instruments'][0]['bondParams']['maturityDate'])))
                    s.assertEqual(text.text, "Дaта погашения облигации")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Дата погашения облигации', {str(formatting_dates(gql_resp['data']['instruments'][0]['bondParams']['maturityDate']))}")
            except NoSuchElementException:
                logging.error("maturityDate not found")
        else:
            pass
        if gql_resp['data']['instruments'][0]['bondParams']['nextCoupon'] not in [0, None]:
            try:
                card = find_by_id(driver, nextCouponDate)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, str(formatting_dates(gql_resp['data']['instruments'][0]['bondParams']['nextCoupon'])))
                    s.assertEqual(text.text, "Дата выплаты купона")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Дата выплаты купона', {str(formatting_dates(gql_resp['data']['instruments'][0]['bondParams']['nextCoupon']))}")
            except NoSuchElementException:
                logging.error("nextCouponDate not found")
        else:
            pass

        if gql_resp['data']['instruments'][0]['bondParams']['couponValue'] not in [0, None]:
            try:
                card = find_by_id(driver, couponValue)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, prices_formatting(
                        gql_resp['data']['instruments'][0]['bondParams']['couponValue']))
                    s.assertEqual(text.text, "Размер купона")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Размер купона', {gql_resp['data']['instruments'][0]['bondParams']['couponValue']}")
            except NoSuchElementException:
                logging.error("couponValue not found")
        else:
            pass

        if gql_resp['data']['instruments'][0]['bondParams']['accruedInt'] not in [0, None]:
            try:
                card = find_by_id(driver, accruedInterest)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text,
                                  prices_formatting(gql_resp['data']['instruments'][0]['bondParams']['accruedInt']))
                    s.assertEqual(text.text, "Накопленный купонный доход")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Накопленный купонный доход', {prices_formatting(gql_resp['data']['instruments'][0]['bondParams']['accruedInt'])}")
            except NoSuchElementException:
                logging.error("accrued interest not found")
        else:
            pass

        if resp['value']['bondData']['bondFaceValue'] not in [0, None]:
            try:
                card = find_by_id(driver, faceValue)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, prices_formatting(resp['value']['bondData']['bondFaceValue']))
                    s.assertEqual(text.text, "Номинал")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Номинал', {prices_formatting(resp['value']['bondData']['bondFaceValue'])}")
            except NoSuchElementException:
                logging.error("maturityYield not found")
        else:
            pass

        if gql_resp['data']['instruments'][0]['bondParams']['couponPeriod'] not in [0, None]:
            try:
                card = find_by_id(driver, couponPeriod)
                price = cond_bond_value(card)
                text = cond_bond_text(card)
                try:
                    s.assertEqual(price.text, str(gql_resp['data']['instruments'][0]['bondParams']['couponPeriod']))
                    s.assertEqual(text.text, "Периодичность выплаты купона")
                except AssertionError:
                    logging.error(
                        f"Actual result: {text.text}, {price.text}, Expected: 'Периодичность выплаты купона', {gql_resp['data']['instruments'][0]['bondParams']['couponPeriod']}")
            except NoSuchElementException:
                logging.error("couponPeriod not found")
        else:
            pass

        driver.swipe(500, 1838, 500, 700)
        try:
            card = find_by_id(driver, open_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
                s.assertEqual(text.text, "Цена открытия")
                s.assertEqual(price.text, prices_formatting(open_bond_counter(resp)))
            except AssertionError:
                logging.error(
                    f"Actual: {text.text}, {price.text}, Expected: 'Цена открытия', {prices_formatting(open_bond_counter(resp))}")
        except NoSuchElementException:
            logging.error(
                "Open price statistics not found")
        try:
            card = find_by_id(driver, close_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
                s.assertEqual(text.text, "Цена закрытия")
                s.assertEqual(price.text, prices_formatting(close_bond_counter(resp)))
            except AssertionError:
                logging.error(
                    f"Actual: {text.text}, {price.text}, Expected: 'Цена закрытия', {prices_formatting(close_bond_counter(resp))}")
        except NoSuchElementException:
            logging.error(
                "Close price statistics not found")
        try:
            card = find_by_id(driver, range_stat)
            price = price_stat_value(card)
            text = price_stat_text(card)
            try:
                s.assertEqual(text.text, "Дневной диапазон")
                if resp['value']['highBid'] and resp['value']['lowAsk'] in [0, None]:
                    s.assertEqual(price.text,
                                  '\u2013')
                else:
                    s.assertEqual(price.text,
                                  f"{prices_formatting(resp['value']['lowAsk'])} - {prices_formatting(resp['value']['highBid'])}")

            except AssertionError:
                if resp['value']['highBid'] in [0, None] and resp['value']['lowAsk'] in [0, None]:
                    logging.error(f"Actual: {text.text}, {price.text}, Expected: 'Дневной диапазон','\u2014'")
                else:
                    logging.error(
                        f"Actual: {text.text}, {price.text}, Expected: 'Дневной диапазон', f'{prices_formatting(resp['value']['lowAsk'])} - {prices_formatting(resp['value']['highBid'])}' ")
        except NoSuchElementException:
            logging.error("Daily range not found")

        driver.find_element_by_accessibility_id('Вернуться назад').click()

    except ConnectionError:
        driver.find_element_by_accessibility_id('Вернуться назад').click()
