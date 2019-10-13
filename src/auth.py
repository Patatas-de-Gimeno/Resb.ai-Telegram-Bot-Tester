from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from imgurpython import ImgurClient
import configparser
import os


def authenticate():
    config = configparser.ConfigParser()
    config.read('auth.ini')

    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')

    imgur_username = config.get('credentials', 'client_user')
    imgur_password = config.get('credentials', 'client_password')

    client = ImgurClient(client_id, client_secret)
    authoritzation_url = client.get_auth_url('pin')

    # This opens the authoritzation url and get the pin
    driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), '../geckodriver'))
    driver.get(authoritzation_url)
    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.send_keys(imgur_username)
    password.send_keys(imgur_password)
    driver.find_element_by_name("allow").click()

    timeout = 5
    try:
        element_present = ec.presence_of_element_located((By.ID, 'pin'))
        WebDriverWait(driver, timeout).until(element_present)
        pin_element = driver.find_element_by_id('pin')
        pin = pin_element.get_attribute("value")
    except TimeoutException:
        print("Timed out waiting for page to load")
    driver.close()

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    print("Authentication successfull")

    return client
