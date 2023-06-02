import time 
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException


# Defining the options for Web Driver #Path in case of Mac Environment can be for example '/usr/local/bin/chromedriver' 
chrome_path = '/usr/local/bin/chromedriver'
chrome_service = Service(chrome_path) 
driver = Chrome(service=chrome_service) 


#Function which extracts relevant data from each Web Element
def extract_data(element): 
    
    #Job Title extracted
    job_titles = element.find_elements(By.TAG_NAME, 'h3')
    if job_titles:
      job_titles = job_titles[0].text
    else:
      job_titles = None 
    
    #Job Position creation date extracted
    creation_dt = element.find_elements(By.TAG_NAME, 'em')
    if creation_dt:
      creation_dt = creation_dt[0].text
    else:
      creation_dt = None  
    
    #Employer for the Position extracted
    employer = element.find_elements(By.CSS_SELECTOR, "span[class*='ecl-u-type-s jv-result-employer-name']")
    if employer:
      employer = employer[0].text
    else:
      employer = None 

    #Job Location extracted
    location = element.find_elements(By.CSS_SELECTOR, "span[class*='jv-result-location-country ng-star-inserted']")
    if location:
      location = location[0].text
    else:
      location = None  

    #Job Type extracted for confirmation
    job_type = element.find_elements(By.CSS_SELECTOR, "span[class*='ecl-u-type-s jv-result-position-schedule-code ng-star-inserted']")
    if job_type:
      job_type = job_type[0].text
    else:
      job_type = None  
    
    #job_link_element = element.find_elements(By.XPATH, '//h3//a')
    #job_link = job_link_element.get_attribute('href') if job_link_element else None


    #Function returns the following values with names of column in the CSV on the left side.
    return {
      "job_titles" : job_titles,
      "Creation date" : creation_dt, 
      "employer" : employer,
      "location" : location,
      "Job_Type" : job_type,
     #"job link" : job_link

    } 

    #Function for denesting lists 
def flatten2 (myList):
	flatList = []
	for item in myList:
		if isinstance(item, list):
			flatList.extend(flatten2(item))
		else:
			flatList.append(item)
	return flatList

# Variable for defining the number of pages for which the code should run. 
# This can be seen selecting the appropriate filters and diving the number of Vacancies by number of results per page. 
# Can be automated by getting the number of vacancies for out particular filters.
num_api_calls = 150

#List for storing the extracted data
extracted_data=[]

start_time = time.time()  # The timer for measuring the time taken to successfully process all the pages starts here.

#For Loop for processing successive pages
for page in range(1, num_api_calls+1):
    print("Page Number:", page)
    driver.get('https://ec.europa.eu/eures/portal/jv-se/search?page={0}&resultsPerPage=50&orderBy=BEST_MATCH&locationCodes=de&keywordsTitle=Data%20Engineer&positionScheduleCodes=fulltime&lang=en'.format(page))
    time.sleep(10)

    content = driver.find_element(By.CSS_SELECTOR, "div[class*='ecl-u-border-top ecl-u-border-color-grey-15'")
    jobs = content.find_elements(By.TAG_NAME, 'jv-result-summary')
    
    # For loop for processing the different job postings in a particular page 
    for job in jobs:
      job_title_element = job.find_element(By.TAG_NAME, 'h3')
      job_title = job_title_element.text
      if 'data engineer' in job_title.lower():  #Condition for checking whether the Keyword Data Engineer is in the Job Title because the Website also gives Bogus results.
        extracted_data.append(extract_data(job))

# Calculate and print the total execution time
execution_time = time.time() - start_time
print("Total execution time:", execution_time, "seconds") 

#Printing the data in a CSV File
if extracted_data:
    df = pd.DataFrame(extracted_data)
    df.to_csv("result150.csv", index=False)