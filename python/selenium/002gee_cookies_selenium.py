# -*- coding: utf-8 -*-
"""
* Updated on 2020/05/24
* python3
**
* cookie for 'SACSID' will expire in 14 days. It is the shortest lifetime in those important keys.
"""

import requests
import time, datetime
import os, sys, json
import random
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def waitPageLoading(method='xpath', content=None, timeout=300):
	if not content:
		print('Error -- "content" can not be None')
		return False
	try:
		if 'XPATH' in method.upper():
			loadPage = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, content)))
		elif 'ID' in method.upper():
			loadPage = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, content)))
		return True
	except:
		return False

def authenticate(username, password):
	options = webdriver.ChromeOptions()
	#options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = Chrome(ChromeDriverManager().install(), options=options)

	try:
		# Using stackoverflow for third-party login & redirect
		url = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27'
		driver.get(url)
		content = '//*[@id="openid-buttons"]/button[1]'
		waitPageLoading(method='xpath', content=content, timeout=300)
		time.sleep(random.randint(2,8))
		driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
		
		content = '//input[@type="email" or @id="identifierId"]'
		waitPageLoading(method='xpath', content=content, timeout=300)
		time.sleep(random.randint(2,8))
		driver.find_element_by_xpath(content).send_keys(username + Keys.RETURN)
		
		content = '//div[@id="password"]//input[@type="password"]'
		waitPageLoading(method='xpath', content=content, timeout=300)
		time.sleep(random.randint(2,8))
		driver.find_element_by_xpath(content).send_keys(password + Keys.RETURN)
		
		content = '//*[@id="content"]'
		waitPageLoading(method='xpath', content=content, timeout=300)
		time.sleep(random.randint(2,8))
		
		driver.get('https://code.earthengine.google.com')
		try:
			content = '//div[@data-identifier="%s"]' %username
			waitPageLoading(method='xpath', content=content, timeout=300)
			driver.find_element_by_xpath(content).click()
			time.sleep(random.randint(2,8))
			
			content = '//*[@id="submit_approve_access"]'
			waitPageLoading(method='xpath', content=content, timeout=300)
			driver.find_element_by_xpath(content).click()
			time.sleep(random.randint(2,8))
		except:
			pass
		finally:
			content = '//div[@id=":1e"]'
			waitPageLoading(method='xpath', content=content, timeout=300)
			time.sleep(random.randint(2,8))
	except Exception as e:
		print(e)
		driver.quit()
		sys.exit('Failed to setup Selenium profile')
	
	cookies = driver.get_cookies()
	s = requests.Session()
	for cookie in cookies:
		s.cookies.set(cookie['name'], cookie['value'])
	r=s.get("https://code.earthengine.google.com/assets/upload/geturl")
	try:
		if r.json()['url']:
			print('\n'+'Selenium Setup complete with Google Profile')
			return cookies
	except Exception as e:
		print(e)
		return False
	finally:
		driver.quit()

if __name__ == '__main__':
	username = 'your username'
	password = 'your password'
	cookies = authenticate(username, password)
	json = json.dumps(cookies)
	with open('gee_cookies.csv','w') as f:
		f.write(json)