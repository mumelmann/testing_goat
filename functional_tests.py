from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://192.168.1.21:8000')

assert 'Django' in browser.title