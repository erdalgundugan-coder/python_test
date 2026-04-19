from gitHubUserInfo import username, password
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Github:
    def __init__(self,username,password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get('https://github.com/login')
        time.sleep(1)
        self.browser.find_element(By.XPATH,'//*[@id="login_field"]').send_keys(self.username)
        self.browser.find_element(By.XPATH,'//*[@id="password"]').send_keys(self.password)
        time.sleep(1)
        self.browser.find_element(By.XPATH,'//*[@id="login"]/div[4]/form/div/input[11]').click()

        time.sleep(5)
        self.browser.close()
        print('bitti')
github = Github(username, password)
github.signIn()


       

   