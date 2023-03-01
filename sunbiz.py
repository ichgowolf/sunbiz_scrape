import os.path
import time
import sys
import re
import csv
from csv import DictWriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup






#  check if csv file exsist if not then creat file and headers
def check_for_file(current_working_directory):
    exsist = os.path.isfile(current_working_directory + "\\active_companies.csv")
    print(current_working_directory)
    print(exsist)
    if exsist:
        return True
    else:
        # assign header columns
        headerList = ["Company Name", "Document Number", "FEI/EIN Number", "Date Filed", "Effective Date", "state"]
        # open CSV File and assign header
        with open(current_working_directory + "\\active_companies.csv", "w", encoding="utf-8") as file:
            dw = csv.DictWriter(file, delimiter=",", fieldnames=headerList)
            dw.writeheader()
            return True
        # display csv file
        fileContent = pd.read_csv("active_companies.csv")
        
        
# apend to csv file
def add_company(current_working_directory, company_name, document_number, fei_ein_number, date_filed, effective_date, state):
    # list of column names
    field_names = ["Company Name", "Document Number", "FEI/EIN Number","Date Filed", "Effective Date", "state"]

    # Dictionary that we want to add as a new row
    dict = {"Company Name": company_name, "Document Number": document_number, "FEI/EIN Number": fei_ein_number,"Date Filed": date_filed, "Effective Date": effective_date, "state": state }
    
    # Open CSV file in append mode
    with open(current_working_directory + "\\active_companies.csv", "a") as f_object:
        
        # Pass the file object and a list
        # of column names to DictWriter()
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
         
        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(dict)
        
        # Close the file object
        f_object.close()




# Get current file path to chromedriver.exe
cwd = os.path.dirname(__file__)
PATH = cwd + "\chromedriver.exe"



if check_for_file(cwd):
    print("file there")
else:
    if check_for_file(cwd):
        print("failed to make file")


# zipCode = input("Enter zip code: ")
zipCode = 33157


# inverse comments below to see browser
# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver = webdriver.Chrome(PATH)

driver.get("http://search.sunbiz.org/inquiry/corporationsearch/byzip")


# find zip code input box
elem = driver.find_element_by_id("SearchTerm")
elem.clear()
elem.send_keys(zipCode)

# search Enter
elem.send_keys(Keys.RETURN)



active_records = []
while 1 == 1:
        
    # Check active or Inactive
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    # Grab list of active an inactive
    all_active = soup.find_all(text="Active")

    done = []
    for active in all_active:
        # gives table row go to company description
        try:
            company_tr = active.find_parent("tr")
            company_name_td = company_tr.contents[1]
            company_name = company_name_td.contents[0].get_text(" ", strip=True)
            # print(company_name)
            driver.find_element_by_link_text(company_name).click()
            time.sleep(5)
        except NoSuchElementException:
            print("fail")
            continue
        
        # soup switch pages 
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # find date filed
        filing_information_all = soup.find("label", text="Date Filed").parent
        
        # filing_information_clean = filing_information.get_text(" ", strip=True)
        comp_name = company_name
        document_number = filing_information_all.contents[2]
        fei_ein_number = filing_information_all.contents[5]
        date_filed = filing_information_all.contents[8]
        effective_date = filing_information_all.contents[9]
        state = filing_information_all.contents[14]
        # status = filing_information_all.contents[17]
        
        # get company info todo add to dattaframe STATUS has been removed
        active_records.append((company_name, document_number, fei_ein_number, date_filed, effective_date, state, ))
        done.append(company_name)
        print(company_name, document_number, fei_ein_number, date_filed, effective_date, state,  )
        
        # exit()
        # print(filing_information_clean)

        add_company(cwd, company_name, document_number, fei_ein_number, date_filed, effective_date, state)
        
        # return to full list
        driver.find_element_by_link_text("Return to List").click()
        
        # soup switch pages 
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
    
    print(active_records)
    # if active_records[-1][-6] == done[-1]:   
    try:
        driver.find_element_by_link_text("Next List").click()
        time.sleep(5)
    except NoSuchElementException: 
        print("The End") 
        break    
    
     


driver.close()
