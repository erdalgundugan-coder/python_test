from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
url = "http://github.com"
driver.get(url)

time.sleep(1)
driver.maximize_window()
#driver.save_screenshot("githup.com-homepage.png")
# url = "https://www.hepsiburada.com"
# driver.get(url)
searchInput =driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]')
print(driver.title)
time.sleep(1)
searchInput.send_keys("python")

# driver.save_screenshot("hepsi-burada.com-homepage.png")
# driver.back()
time.sleep(1)
searchInput.send_keys(Keys.ENTER)

time.sleep(1)
result = driver.find_elements(By.CLASS_NAME, 'f4')
for es in result:
    print(es.text)
#time.sleep(4)
time.sleep(1)
driver.close()
