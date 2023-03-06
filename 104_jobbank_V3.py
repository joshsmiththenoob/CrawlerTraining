# 104_job_bank with Selenium (Overview)
# import packages
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv , time ,sys

def create_driver():
    service = Service("./chromedriver")
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    driver = Chrome(service=service,options = chrome_options)
    return driver

# func : access job page
def access_job_page(job_table,job_link):
    print(f'========== 工作連結為{job_link} ================')
    # service = Service("./chromedriver")
    # chrome_options = Options()
    # chrome_options.page_load_strategy = 'eager'
    driver2 = create_driver()
    driver2.get(job_link)
    # slide simulation
    driver2.execute_async_script(
        """
    count = 400;
    let callback = arguments[arguments.length - 1];
    t = setTimeout(function scrolldown(){
        console.log(count, t);
        window.scrollTo(0, count);
        if(count < (document.body.scrollHeight || document.documentElement.scrollHeight)){
        count+= 400;
        t = setTimeout(scrolldown, 1000);
        }else{
        callback((document.body.scrollHeight || document.documentElement.scrollHeight));
        }
    }, 1000);"""
    )
    
    # get job's info
    job_table = append_job(job_table,driver2)
    
    time.sleep(3)
    driver2.close()
    return job_table

# func : get job's info and save into dataframe
def append_job(job_table,driver2):
    company_name= driver2.find_element(By.CLASS_NAME, "btn-link.t3.mr-6").text
    job_name = driver2.find_element(By.CLASS_NAME, "pr-6.text-break").text
    job_type = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[0].text.replace("\n","")
    job_pay = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[1].text
    ft_pt = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[2].text
    job_location = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[3].text
    job_content = driver2.find_element(By.CLASS_NAME, "mb-5.r3.job-description__content.text-break").text
    if len(job_content) > 500 :
        job_content = job_content[:500]
        job_content += ".....詳情請見網站"
    subject = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[13].text
    job_tools = driver2.find_elements(By.CLASS_NAME, "col.p-0.list-row__data")[15].text.split('\n')[0]
    another_require = driver2.find_elements(By.CLASS_NAME,"col.p-0.list-row__data")[-1].text
    each_job_detail = {
                   "company_name" : company_name,
                   "job_name" : job_name,
                   "job_type" : job_type,
                   "job_pay" : job_pay,
                   "ft_pt" : ft_pt,
                   "job_location" : job_location,
                   "subject" : subject,
                   "job_tools" : job_tools,
                   "job_content" : job_content,
                   "another_require" : another_require
                    }
    each_job_table = pd.DataFrame([each_job_detail])
    job_table = pd.concat([job_table,each_job_table], ignore_index=True)
    return job_table


    
def main():
    # Get Driver
    driver = create_driver()

    # 104 home page's url
    url = "https://www.104.com.tw/jobs/main/"  # go to jobbank
    driver.get(url) # surf jobbank with browser
    driver.maximize_window() # maximize broswer window -> get more HTML ASAP
    time.sleep(3)

    # KeyWord of interest
    driver.find_element(by=By.XPATH, value='/html/body/article[1]/div/div/div[4]/div/input').send_keys("Python工程師")
    time.sleep(3)

    # Push search button
    driver.find_element(by=By.XPATH,value='/html/body/article[1]/div/div/div[4]/div/button').click()
    time.sleep(3)

    # Scroll action
    # Step 1 : get all pages' count
    button = driver.find_element(By.CLASS_NAME,"b-clear-border.page-select.js-paging-select.gtm-paging-bottom")
    Total_pages_count = len(button.text.split("\n"))

    # Step 2 : auto scroll + manual scroll
    manual_scroll_count = 1
    request_nth = input("請問要搜尋幾個職缺? :")
    first_counts = len(driver.find_elements(By.CLASS_NAME, "js-job-link")) # get counts of 1st page's job

    # Step 3 : create job_table in beggining
    job_table = pd.DataFrame() # create empty table

    # Step 4 : crawling info of jobs and writing it into job_table(DataFrame)
    while manual_scroll_count :
        if manual_scroll_count + 15 == Total_pages_count:
            print("================ 已到達最底，翻頁完成 !!=======================")
            break
        jobs = driver.find_elements(By.CLASS_NAME, "js-job-link")
        print(f"================ 目前共有{len(jobs)}個職缺 ===================")
        if (len(jobs) - first_counts) / 20 + 1 == 1: # if 1st page
            for nth,job in enumerate(jobs,start = 1):
                driver.execute_script("arguments[0].scrollIntoView();",job) # slide to target elem
                driver.execute_script("window.scrollBy(0, -240);")
                job_link = job.get_attribute("href")
                print(f'===============這是第{nth}個工作 ===================')
                job_table = access_job_page(job_table,job_link)
                if str(nth) == request_nth:
                    print(f"============= 已爬取 {nth} 個職缺，停止服務 !! ===============")
                    manual_scroll_count = 0
                    break
                
        else : # another page
            for nth,job in enumerate(jobs[-20:],start = len(jobs)- (20 + 1)): # get last 20 jobs
                driver.execute_script(f"arguments[0].scrollIntoView();",job)  # slide to target elem
                driver.execute_script("window.scrollBy(0, -240);")
                job_link = job.get_attribute("href")
                print(f'===============這是第{nth}個工作 ===================')
                job_table = access_job_page(job_table,job_link)
                if str(nth) == request_nth:
                    print(f"============= 已爬取 {nth} 個職缺，停止服務 !! ===============")
                    manual_scroll_count = 0
                    break
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        try:
            button = driver.find_element(By.CLASS_NAME,"b-btn.b-btn--link.js-more-page")
            driver.execute_script("arguments[0].click();", button)
            print(f"================ 需要手動!! 按一下按鈕! -> 目前翻到第{manual_scroll_count + 15} 頁=================")
            manual_scroll_count += 1
            time.sleep(2)
        except Exception :
            print("================ 不用手動，繼續滑下去!! 直到翻到第15頁 =================")
    job_table.to_csv("test.csv",index=False) # 不顯示索引值並儲存至csv

if __name__ == "__main__":
    main()