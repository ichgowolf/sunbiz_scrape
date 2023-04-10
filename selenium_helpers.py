import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from csv_handler import add_company


def setup_driver(chromedriver_path, headless=True):
    """
    Initialize and configure a Chrome WebDriver instance.

    This function creates a new Chrome WebDriver instance with the given
    chromedriver_path, and configures it to run in headless mode if the
    'headless' parameter is set to True.

    :param chromedriver_path: The file path to the ChromeDriver executable.
    :param headless: A boolean value indicating whether to run the WebDriver in headless mode (default is True).
    :return: A configured Chrome WebDriver instance.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(chromedriver_path, options=options)


def get_company_data(soup, company_name):
    
    """
    Extract the relevant company information from the BeautifulSoup object.

    This function extracts the company's document number, FEI/EIN number,
    date filed, effective date, and state from the provided BeautifulSoup
    object, and combines them with the provided company_name to create a
    dictionary containing the company data.

    :param soup: A BeautifulSoup object containing the company information.
    :param company_name: The name of the company.
    :return: A dictionary containing the company's data.
    """

    filing_information = soup.find("label", string="Date Filed").parent

    company_data = {
        "Company Name": company_name,
        "Document Number": filing_information.contents[2],
        "FEI/EIN Number": filing_information.contents[5],
        "Date Filed": filing_information.contents[8],
        "Effective Date": filing_information.contents[9],
        "state": filing_information.contents[14]
    }

    return company_data





def process_active_companies(driver, cwd):
    """
    Process the active companies on the current web page and add them to the CSV file.

    This function will go through all the active companies in the current page, click
    on their links, extract relevant information using the get_company_data function,
    and then add the extracted data to the CSV file using the add_company function.

    :param driver: Selenium WebDriver instance used to interact with the web page.
    :param cwd: The current working directory where the active_companies.csv file is located.
    :raises: NoSuchElementException if any company link is not found during the process.
    """
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    active_labels = soup.find_all(string="Active")

    for active in active_labels:
        try:
            company_tr = active.find_parent("tr")
            company_name_td = company_tr.contents[1]
            company_name = company_name_td.contents[0].get_text(" ", strip=True)
            driver.find_element_by_link_text(company_name).click()
            time.sleep(5)
        except NoSuchElementException:
            print("Click failed")
            continue

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        company_data = get_company_data(soup, company_name)

        add_company(cwd, company_data)

        driver.find_element_by_link_text("Return to List").click()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')



def navigate_to_next_page(driver):
    """
    Navigate to the next page of results by clicking the "Next List" link.

    :param driver: Selenium WebDriver instance used to interact with the web page.
    :return: True if the "Next List" link is found and clicked, False otherwise.
    :raises: NoSuchElementException if the "Next List" link is not found.
    """
    try:
        driver.find_element_by_link_text("Next List").click()
        time.sleep(5)
    except NoSuchElementException:
        print("The End")
        return False
    return True