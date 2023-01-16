from functions import *
from urls import *
from selenium.common.exceptions import NoSuchElementException
import logging
from paths import *


def card_companydataview(s, driver, name, gql_body):
    try:
        driver.find_element_by_android_uiautomator(
            f'new UiSelector().className("android.widget.TextView").resourceId('
            f'"ru.sberbank.investor.dev:id/title").text("{name}")').click()
        resp = call_url_post(graphQl_url, gql_body)
        driver.swipe(500, 1838, 500, 700)
        try:
            driver.find_element_by_accessibility_id("Обзор").click()
            try:
                s.assertEqual(find_by_id(driver, companyTitle).text, resp['data']['instruments'][0]['companyData']['basicName'])
            except NoSuchElementException:
                logging.error("CompanyData not found")
            except AssertionError:
                logging.error(f"Actual: {find_by_id(driver, companyTitle).text}, Expected: {resp['data']['instruments'][0]['companyData']['basicName']}")
            try:
                card = find_by_id(driver, sector)
                text = cond_bond_text(card)
                value = cond_bond_value(card)
                try:
                    s.assertEqual(text.text, "Отрасль")
                    s.assertEqual(value.text, resp['data']['instruments'][0]['companyData']['sectorName'])
                except AssertionError:
                    logging.error(f"Actual: {text.text} {value.text}, Expected: Отрасль, {resp['data']['instruments'][0]['companyData']['sectorName']}")

            except NoSuchElementException:
                logging.error("sector not found")
            try:
                card = find_by_id(driver, country)
                text = cond_bond_text(card)
                value = cond_bond_value(card)
                try:
                    s.assertEqual(text.text, "Страна")
                    s.assertEqual(value.text, resp['data']['instruments'][0]['companyData']['ruCountryName'])
                except AssertionError:
                    logging.error(
                        f"Actual: {text.text} {value.text}, Expected: Отрасль, {resp['data']['instruments'][0]['companyData']['ruCountryName']}")

            except NoSuchElementException:
                logging.error("country not found")
            try:
                card = find_by_id(driver, exchange)
                text = cond_bond_text(card)
                value = cond_bond_value(card)
                try:
                    s.assertEqual(text.text, "Биржа")
                    if resp['data']['instruments'][0]['exchange'] == 'MOEX':
                        s.assertEqual(value.text, "Московская биржа")
                    elif resp['data']['instruments'][0]['exchange'] == 'OTC':
                        s.assertEqual(value.text, "Внебиржевые торги")
                except AssertionError:
                    logging.error(
                        f"Actual: {text.text} {value.text}, Expected: Биржа, {resp['data']['instruments'][0]['exchange']}")

            except NoSuchElementException:
                logging.error("country not found")

            if resp['data']['instruments'][0]['companyData']['regDate'] not in [0, None]:
                try:
                    card = find_by_id(driver, foundation_date)
                    text = cond_bond_text(card)
                    value = cond_bond_value(card)
                    try:
                        s.assertEqual(text.text, "Год основания")
                        s.assertEqual(value.text, formatting_dates_only_year(resp['data']['instruments'][0]['companyData']['regDate']))
                    except AssertionError:
                        logging.error(f"Actual: {text.text}, {value.text}, Expected: 'Год основания' {formatting_dates_only_year(resp['data']['instruments'][0]['companyData']['regDate'])}")
                except NoSuchElementException:
                    logging.error("foundation date not found")

        except NoSuchElementException:
            logging.error("Вкладка 'Обзор' не найдена")
        driver.find_element_by_accessibility_id('Вернуться назад').click()

    except ConnectionError:
        driver.find_element_by_accessibility_id('Вернуться назад').click()