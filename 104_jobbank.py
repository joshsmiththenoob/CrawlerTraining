from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import csv

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

# 將Selenium滑動(更新)後的HTML結果交給BS4解析
soup = BeautifulSoup(driver.page_source,"html.parser") #html以utf-8形式解碼 成為"字串檔案" → 而後以bs解析成為真正的html標籤檔案

# print(soup)

# 找工作
job_list = soup.findAll('a',{'class':'js-job-link'})
# print(type(logo_tag_list))
joblist = []
for job_object in job_list:
    joblist.append(job_object.text)

print(joblist)
# 找公司
company_list = soup.select('.b-list-inline.b-clearfix') # 選擇大標籤
companylist = []
for company_object in company_list:
    # company = company_object
    company = company_object.select_one('a') #從大標籤內再篩選小標籤 (找屬性class有.b-list-inline.b-clearfix的標籤)
    if company == None: #
        continue
    companylist.append(company.text.split('\n')[0])
    # print(f'{company.text},{type(company.text)}')

print(companylist)

# 找工作內容
content_list = soup.select('.b-block__left')
contentlist = []
# print(content_list)
for content_object in content_list:
    content = content_object.select_one('p') #從大標籤內再篩選小標籤 (找屬性class有.b-list-inline.b-clearfix的標籤)不再是列表，而是element    if content == '':
    a = content.text
    if a == '':  #
        continue
    contentlist.append(a)
print(contentlist,len(contentlist))

headers = ['工作','公司','內容']

with open('./104_jobbank.csv','w',newline='',encoding = "utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for i in range(len(joblist)):
        writer.writerow([joblist[i],companylist[i],contentlist[i]])