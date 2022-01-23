import time
import pandas
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def contacts(cl_name):
    contacts_df = pandas.read_excel(f'{cl_name}.xlsx')
    return contacts_df

def select_browser(browser_name):
    browser = getattr(webdriver, browser_name)()
    return browser

def open_browser_url(browser, url):
    browser.get(url)

    while len(browser.find_elements(By.ID, 'side')) < 1:
        time.sleep(1)

def send_messages(contacts_df, browser, wait_time):
    for i, msg in enumerate(contacts_df['Message']):
        name = contacts_df.loc[i, 'Name']
        number = contacts_df.loc[i, 'Number']
        message = urllib.parse.quote(f'Hello, {name}! {msg}')
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'

        open_browser_url(browser, url)
        browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
        time.sleep(wait_time)

def execution(cl_name, browser, wait_time):
    contacts_df = contacts(cl_name)
    browser = select_browser(browser)
    open_browser_url(browser, 'https://web.whatsapp.com/')
    send_messages(contacts_df, browser, wait_time)

execution('contacts_list', 'Chrome', 10)