from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller
import random
from datetime import datetime
import pytz;  beijing = pytz.timezone('Asia/Chongqing')

username = 'your username'
password = 'your password'

#check and install chromedriver automatically
chromedriver_autoinstaller.install()

#set chrome options
chrome_options = webdriver.ChromeOptions()	#from selenium.webdriver.chrome.options import Options as ChromeOptions
chrome_options.headless = True	#withou open a real browser
'''
#disable images with browser
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
'''

browser = webdriver.Chrome(options=chrome_options)
#browser = webdriver.Chrome('/mnt/c/Windows/System32/chromedriver', options=chrome_options)	#for my wsl

url = 'https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do%3Ft_s%3D1588030135809%26amp_sec_version_%3D1%26gid_%3DR2V3dzJPY2FPeWJYbGk5dXZ0UXdSSjFuODRONkpPTnFuUzQrVXM1Vi9lV3pPS1JQVlRiSERqMkhTVVBaZ0lzWW9OUERPMWkrZnlYQlZpL2U1OVN6elE9PQ%26EMAP_LANG%3Dzh%26THEME%3Dindigo%23%2FdailyReport'

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

def login(username, password):
	while True:
		browser.get(url)
		#wait for page-loading
		loadPage = waitPageLoading(method='id', content='casLoginForm')
		if not loadPage:
			browser.quit()
			continue
		
		#input username
		usernameBox = browser.find_element_by_id('username')
		usernameBox.send_keys(username)
		#input password
		passwordBox = browser.find_element_by_id('password')
		passwordBox.send_keys(password)
		#sign in
		signinButton = browser.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button')		
		if signinButton:
			signinButton.click()
			print('Login successfully')
			return True
		else:
			print('Login failed, try again')
			browser.quit()

def checkReport(date):
	#wait for page-loading
	while True:
		loadPage = waitPageLoading(method='xpath', content='//*[contains(text(),"详情")]')
		if not loadPage:
			browser.refresh; continue
		else:
			break
	#check if current report exists
	try:
		firstRecord = browser.find_element_by_xpath('//*[contains(text(),"%s")]' % date)
		if firstRecord:
			print('Report exists : %s' % firstRecord.text)
			browser.quit()
			return True
	except:
		return False

def addReport(username, password):
	while True:
		date = datetime.now(beijing).strftime('%Y-%m-%d')
		
		#check if exist
		check = checkReport(date)
		if check:
			return True
		
		#click add/new
		newButton = browser.find_element_by_xpath('//div[text()="新增"]')
		if not newButton:
			browser.refresh(); continue
		newButton.click()
		
		#entry new report
		#wait for page-loading
		loadPage = waitPageLoading(method='xpath', content='//div/div[1]/section/div[2]/div/div[4]/div[2]/div[1]/div/div/input')
		if not loadPage:
			browser.refresh; continue
			
		temperatureBox = browser.find_element_by_xpath('//div/div[1]/section/div[2]/div/div[4]/div[2]/div[1]/div/div/input')
		temperature = str(round(random.uniform(36.8,37.4),1))
		temperatureBox.send_keys(temperature)
		
		#save
		saveButton = browser.find_element_by_id('save')
		if not saveButton:
			browser.refresh(); continue
		saveButton.click()
		
		#confirm part
		#wait for page-loading
		loadPage = waitPageLoading(method='id', content='bh-dialog-exceptBtn-con')
		if not loadPage:
			browser.refresh; continue
		
		confirmButton = browser.find_element_by_link_text('确认')
		if not confirmButton:
			browser.refresh(); continue
		confirmButton.click()
		
		#check again
		browser.refresh()
		check = checkReport(date)
		if check:
			return True

if __name__ == '__main__':
	login(username, password)
	addReport(username, password)
