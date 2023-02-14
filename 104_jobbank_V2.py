# 104_job_bank with Selenium
# import packages
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv , time


service = Service("./chromedriver")
driver = Chrome(service=service)

url = "https://www.104.com.tw/jobs/main/"  # go to jobbank
driver.get(url) # 以網頁瀏覽器開啟網址
time.sleep(3)
driver.find_element(by=By.XPATH, value='/html/body/article[1]/div/div/div[4]/div/input').send_keys("光學工程師")
time.sleep(3)

# 按下查詢按鈕
driver.find_element(by=By.XPATH,value='/html/body/article[1]/div/div/div[4]/div/button').click()

# 將網頁畫面往下滾動至離頂部 5000 高度的位子
driver.execute_script('var s = document.documentElement.scrollTop=5000') # Java語言:可以直接把()內指令複製到開發人員→Console最下方comment window進行操作
time.sleep(3)

# 將網頁畫面滾到最上方
driver.execute_script('var s = document.documentElement.scrollTop=0')
time.sleep(3)

