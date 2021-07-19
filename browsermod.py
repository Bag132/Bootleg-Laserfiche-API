import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\\Users\\Victor\\Documents\\chromedriver.exe')
login_url = 'https://accounts.laserfiche.com/WebSTS/Login?originalPathAndQuery=%2fWebSTS%2f%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fapp.laserfiche.com%252flaserfiche%252f%26wctx%3drm%253d1%2526id%253dpassive%2526ru%253d%25252flaserfiche%25252fBrowse.aspx%25253fdb%25253dr-052ecf80%26wct%3d2021-07-14T01%253a00%253a50Z%26wreply%3dhttps%253a%252f%252fapp.laserfiche.com%252flaserfiche%252f%26db%3dr-052ecf80#?id=392585'

if __name__ == '__main__':
	driver.get(login_url)
	print(driver.title)
	account_id_field = driver.find_element_by_class_name('form-entry-value')
	account_id_field.send_keys('672803730')
	account_id_field.send_keys(Keys.RETURN)

	time.sleep(0.5)
	name_field = driver.find_element_by_id('nameField')
	name_field.send_keys('vlomba')

	password_field = driver.find_element_by_id('passwordField')
	password_field.send_keys('Victor132')
	password_field.send_keys(Keys.RETURN)

	time.sleep(5)

	dropdown = driver.find_elements_by_class_name('entryName')
	letter_folders = []


	def refreshLetterFolders(): # Change to use IDs instead so that the WebElements do change
		letter_folders.clear()
		dropdown = driver.find_elements_by_class_name('entryName')
		for streetnamespan in dropdown:
			text = streetnamespan.text
			match = re.findall('[a-zA-Z]{2}', text)

			if len(match) == 0:
				print(text)
				letter_folders.append(streetnamespan)


	refreshLetterFolders()

	print('Bruh\n')

	for i in range(0, len(letter_folders)):
		refreshLetterFolders()
		f = letter_folders[i]
		print('Got address dir: ' + f.text)
		ngcelltext = f.find_element_by_xpath('..')
		row = ngcelltext.find_element_by_xpath('..')
		expand_arrow = row.find_element_by_class_name('expandArrow')
		expand_arrow.click()
		refreshLetterFolders()

