from gitHubUserInfo import username,password
from selenium import webdriver
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Github:
    def __init__(self,username,password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.repository = []
    def singIn(self):
        self.browser.get('https://github.com/login')
        time.sleep(1)
        self.browser.find_element(By.XPATH,'//*[@id="login_field"]').send_keys(username)
        self.browser.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
        time.sleep(1)
        self.browser.find_element(By.XPATH,'//*[@id="login"]/div[4]/form/div/input[11]').click()
    def getRepository(self):

        self.repository = self.browser.find_elements(By.CSS_SELECTOR,'li')
        for i in self.repository:
            i = 
        print(self.repository)
            #print(len(self.repository))

doldur = Github(username,password)
doldur.singIn()
print('bitti')
time.sleep(5)
#doldur.browser.close()
time.sleep(10)
doldur.getRepository()
print('bitti')
time.sleep(10)