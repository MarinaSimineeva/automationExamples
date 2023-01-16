from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import json
import datetime


def call_url_post(url, body):
    response = requests.post(url, json.dumps(body))
    resp_body = json.loads(response.content)
    return resp_body


def call_url_get(url):
    response = requests.get(url)
    resp_body = json.loads(response.content)
    return resp_body


def mdata_resp_filtration(responce):
    # reusable method that takes full response body of mdata and returnes only fields needed
    list_data = responce['resp']['data']
    new_list = [
        {'ticker': i['key']['ticker'], 'lastPrice': i['value']['lastPrice'], 'closePrice': i['value']['closePrice'],
         'bid': i['value']['bid'], 'offer': i['value']['offer']} for i in list_data]
    return new_list


def absolute_value(mdata_dict):
    if mdata_dict['closePrice'] == 0:
        abs_price = 0
        return abs_price
    elif mdata_dict['lastPrice'] != 0:
        abs_price = mdata_dict['lastPrice'] - mdata_dict['closePrice']
        return round(abs_price, 3)
    elif mdata_dict['lastPrice'] == 0 and mdata_dict['bid'] != 0:
        abs_price = mdata_dict['bid'] - mdata_dict['closePrice']
        return round(abs_price, 3)
    elif mdata_dict['lastPrice'] == 0 and mdata_dict['bid'] == 0 and mdata_dict['offer'] != 0:
        abs_price = mdata_dict['offer'] - mdata_dict['closePrice']
        return round(abs_price, 3)
    else:
        abs_price = 0
        return abs_price


def refer_change_value(mdata_dict):
    if mdata_dict['closePrice'] in [0, None]:
        ref_price = 0
        return ref_price
    elif mdata_dict['lastPrice'] not in [0, None]:
        ref_price = (mdata_dict['lastPrice'] - mdata_dict['closePrice']) / mdata_dict['closePrice'] * 100
        if ref_price == 0:
            return ref_price
        else:
            return round(ref_price, 2)
    elif mdata_dict['lastPrice'] in [0, None] and mdata_dict['bid'] not in [0, None]:
        ref_price = (mdata_dict['bid'] - mdata_dict['closePrice']) / mdata_dict['closePrice'] * 100
        if ref_price == 0:
            return ref_price
        else:
            return round(ref_price, 2)
    elif mdata_dict['lastPrice'] in[0, None] and mdata_dict['bid'] in [0, None] and mdata_dict['offer'] not in [0, None]:
        ref_price = (mdata_dict['offer'] - mdata_dict['closePrice']) / mdata_dict['closePrice'] * 100
        if ref_price == 0:
            return ref_price
        else:
            return round(ref_price, 2)
    else:
        ref_price = 0
        return ref_price


def value_idxs_RTS_IMOEX(mdata_dict):
    # counts values for RTS and IMOEX idxs (from mdata dictionary)
    if mdata_dict['closePrice'] not in [0, None] and mdata_dict['lastPrice'] not in [0, None]:
        ref_price = (mdata_dict['lastPrice'] - mdata_dict['closePrice']) / mdata_dict['closePrice'] * 100
        if ref_price == 0:
            return ref_price
        elif ref_price > 0:
            return f"+{str(round(ref_price, 2)).replace('.', ',')} %"
        elif ref_price < 0:
            return f"{str(round(ref_price, 2)).replace('.', ',')} %"
    elif mdata_dict['lastPrice'] not in [0, None] and mdata_dict['closePrice'] in [0, None]:
        ref_price = mdata_dict['lastPrice']
        return f"{str(round(ref_price, 2)).replace('.', ',')} %"
    elif mdata_dict['lastPrice'] in [0, None] and mdata_dict['closePrice'] not in [0, None]:
        ref_price = mdata_dict['closePrice']
        return f"{str(round(ref_price, 2)).replace('.', ',')} %"
    else:
        return '-'


def idxs_prices(data_list):
    # returnes prices displayed for idxs
    result = []
    for f in data_list:
        if f['ticker'] in ('RTSI', 'IMOEX'):
            result.append({'ticker': f['ticker'], 'price': value_idxs_RTS_IMOEX(f)})
        elif f['ticker'] in ('BRN2', 'BRM2', 'BRK2'):
            result.append({'ticker': f['ticker'], 'price': f"{str(round(f['lastPrice'], 2)).replace('.', ',')} $"})
        else:
            result.append({'ticker': f['ticker'], 'price': f"{str(round(f['lastPrice'], 2)).replace('.', ',')} RUB"})
    return result


# formatting methods


def prices_formatting(price):
    if price != '-':
        price = round(price, 3)
        price_str = ('{:,}'.format(price).replace(',', ' '))
        return f"{str(price_str).replace('.', ',')} ₽"
    else:
        return '\u2014'


def formatting_abs_price_change(abs_price_ch):
    return f"{str(abs(abs_price_ch)).replace('.', ',')} ₽"


def formatting_ref_price_change(ref_price_ch):
    return f"{str(abs(ref_price_ch))} %"


def formatting_dates(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")


def formatting_dates_only_year(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y г.")


# frequently used methods for finding ui elements


def find_by_id(dr, locator):
    dr.find_element(By.ID, locator)
    return dr.find_element(By.ID, locator)


def find_by_xpath(dr, locator):
    return dr.find_element(By.XPATH, locator)


def wait_till_find_id(dr, locator):
    WebDriverWait(dr, 30).until(EC.presence_of_element_located((By.ID, f'{locator}')))
    return dr.find_element(By.ID, locator)


def wait_till_find_xpath(dr, locator):
    WebDriverWait(dr, 30).until(EC.presence_of_element_located((By.XPATH, f'{locator}')))
    return dr.find_element(By.XPATH, locator)


def find_clickable_xpath(xpath):
    EC.element_to_be_clickable((By.XPATH, {xpath}))


def find_clickable_id(id):
    EC.element_to_be_clickable((By.ID, {id}))


def find_index_price(card):
    price = card.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("ru.sberbank.investor.dev:id/text_price")')
    return price


# locating text and values for Statistics block in card's details


def price_stat_value(card):
    value = card.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("ru.sberbank.investor.dev:id/value")')
    return value


def price_stat_text(card):
    value = card.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("ru.sberbank.investor.dev:id/title")')
    return value


# locating text and values for bonds


def cond_bond_text(card):
    value = card.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("ru.sberbank.investor.dev:id/left_text_view")')
    return value


def cond_bond_value(card):
    value = card.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("ru.sberbank.investor.dev:id/right_text_view")')
    return value


# bond prices counting functions


def last_price_bond_counter(resp):
    if resp['value']['lastPrice'] != 0:
        lastPrice = resp['value']['lastPrice'] / 100 * resp['value']['bondData']['bondFaceValue']
        return lastPrice
    elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] != 0:
        lastPrice = resp['value']['bid'] / 100 * resp['value']['bondData']['bondFaceValue']
        return lastPrice
    elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] == 0 and resp['value']['offer'] != 0:
        lastPrice = resp['value']['offer'] / 100 * resp['value']['bondData']['bondFaceValue']
        return lastPrice
    elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] == 0 and resp['value']['offer'] == 0 and \
            resp['value']['closePrice'] != 0:
        lastPrice = resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue']
        return lastPrice
    else:
        lastPrice = '-'
        return lastPrice


def bid_bond_counter(resp):
    if resp['value']['tradingStatus'] == 'TRADING_NOT_AVAILABLE':
        bid = '-'
        return bid
    else:
        if resp['value']['bid'] == 0:
            bid = 'нет котировок'
            return bid
        else:
            bid = resp['value']['bid'] / 100 * resp['value']['bondData']['bondFaceValue']
            return bid


def offer_bond_counter(resp):
    if resp['value']['tradingStatus'] == 'TRADING_NOT_AVAILABLE':
        offer = '-'
        return offer
    else:
        if resp['value']['offer'] == 0:
            offer = 'нет котировок'
            return offer
        else:
            offer = resp['value']['offer'] / 100 * resp['value']['bondData']['bondFaceValue']
            return offer


def absolute_bond_value(resp):
    if resp['value']['closePrice'] == 0:
        abs_price = 0
        return abs_price
    else:
        if resp['value']['lastPrice'] != 0:
            abs_price = (resp['value']['lastPrice'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue'])
            return round(abs_price, 3)
        elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] != 0:
            abs_price = (resp['value']['bid'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue'])
            return round(abs_price, 3)
        elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] == 0 and resp['value']['offer'] != 0:
            abs_price = (resp['value']['offer'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue'])
            return round(abs_price, 3)
        else:
            abs_price = 0
            return abs_price


def ref_bond_value(resp):
    if resp['value']['closePrice'] == 0:
        ref_price = 0
        return ref_price
    else:
        if resp['value']['lastPrice'] != 0:
            ref_price = (resp['value']['lastPrice'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue']) / (
                                resp['value']['closePrice'] / 100 * resp['value']['bondData'][
                            'bondFaceValue']) * 100
            return round(ref_price, 3)
        elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] != 0:
            ref_price = (resp['value']['bid'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue']) / (
                                resp['value']['closePrice'] / 100 * resp['value']['bondData'][
                            'bondFaceValue']) * 100
            return round(ref_price, 3)
        elif resp['value']['lastPrice'] == 0 and resp['value']['bid'] == 0 and resp['value']['offer'] != 0:
            ref_price = (resp['value']['offer'] / 100 * resp['value']['bondData']['bondFaceValue']) - (
                    resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue']) / (
                                resp['value']['closePrice'] / 100 * resp['value']['bondData'][
                            'bondFaceValue']) * 100
            return round(ref_price, 3)
        else:
            ref_price = 0
            return ref_price


def close_bond_counter(resp):
    if resp['value']['closePrice'] in [0, None]:
        close = '-'
        return close
    else:
        close = resp['value']['closePrice'] / 100 * resp['value']['bondData']['bondFaceValue']
        return close


def open_bond_counter(resp):
    if resp['value']['open'] in [0, None]:
        openpr = '-'
        return openpr
    else:
        openpr = resp['value']['open'] / 100 * resp['value']['bondData']['bondFaceValue']
        return openpr
