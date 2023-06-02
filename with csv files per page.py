import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

#to be used in case of without headless browsing

chrome_path = '/usr/local/bin/chromedriver'
chrome_service = Service(chrome_path) 
driver = Chrome(service=chrome_service) 


#to be used in case of headless browsing
# options = webdriver.ChromeOptions() 
# options.headless = True  # Run Chrome in headless mode
# options.page_load_strategy = 'none' 
# chrome_path = 'F:\Downloads\chromedriver_win32\chromedriver'
# chrome_service = Service(chrome_path) 
# driver = Chrome(options=options, service=chrome_service) 
# driver.implicitly_wait(5)



def extract_data(element): 
    job_titles = element.find_elements(By.TAG_NAME, 'h3')
    if job_titles:
      job_titles = job_titles[0].text
    else:
      job_titles = None 

    creation_dt = element.find_elements(By.TAG_NAME, 'em')
    if creation_dt:
      creation_dt = creation_dt[0].text
    else:
      creation_dt = None  

    employer = element.find_elements(By.CSS_SELECTOR, "span[class*='ecl-u-type-s jv-result-employer-name']")
    if employer:
      employer = employer[0].text
    else:
      employer = None 

    location = element.find_elements(By.CSS_SELECTOR, "span[class*='jv-result-location-country ng-star-inserted']")
    if location:
      location = location[0].text
    else:
      location = None  

    job_type = element.find_elements(By.CSS_SELECTOR, "span[class*='ecl-u-type-s jv-result-position-schedule-code ng-star-inserted']")
    if job_type:
      job_type = job_type[0].text
    else:
      job_type = None  
    
    #job_link_element = element.find_elements(By.XPATH, '//h3//a')
    #job_link = job_link_element.get_attribute('href') if job_link_element else None


    return {
      "job_titles" : job_titles,
      "Creation date" : creation_dt, 
      "employer" : employer,
      "location" : location,
      "Job_Type" : job_type,
        # "Industry": ,
      #"job link" : job_link

    } 


def flatten2 (myList):
	flatList = []
	for item in myList:
		if isinstance(item, list):
			flatList.extend(flatten2(item))
		else:
			flatList.append(item)
	return flatList


num_api_calls = 50

#jobsnew=[]
extracted_data=[]
start_time = time.time()  # Start the timer here

for page in range(1, num_api_calls + 1):
    print("Page Number:", page)
    driver.get('https://ec.europa.eu/eures/portal/jv-se/search?page={0}&resultsPerPage=50&orderBy=BEST_MATCH&locationCodes=de&keywordsEverywhere=Data%20Engineer&positionScheduleCodes=fulltime&lang=en'.format(page))
    time.sleep(10)

    try:
        content = driver.find_element(By.CSS_SELECTOR, "div[class*='ecl-u-border-top ecl-u-border-color-grey-15'")
        jobs = content.find_elements(By.TAG_NAME, 'jv-result-summary')
        
        for job in jobs:
            job_title_element = job.find_element(By.TAG_NAME, 'h3')
            job_title = job_title_element.text
            if 'data engineer' in job_title.lower():
                extracted_data.append(extract_data(job))
        
        if extracted_data:
            df = pd.DataFrame(extracted_data)
            df.to_csv("result{0}.csv".format(page), index=False)
    
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Skipping page", page)
        continue

# Calculate and print the total execution time
execution_time = time.time() - start_time
print("Total execution time:", execution_time, "seconds")
