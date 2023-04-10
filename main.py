import os.path
from selenium.webdriver.common.keys import Keys
from csv_handler import check_for_file, add_company
from selenium_helpers import setup_driver, process_active_companies, navigate_to_next_page

def user_input(test = False):
    if test is True:
        return 33157
    else:
        zip_input = input("Enter zip code: ")
        return zip_input


def main():
    cwd = os.path.dirname(__file__)
    chromedriver_path = os.path.join(cwd, "chromedriver.exe")

    if not check_for_file(cwd):
        print("Failed to make file")

    zip_input = user_input(test = True)

    driver = setup_driver(chromedriver_path, headless=False)

    driver.get("http://search.sunbiz.org/inquiry/corporationsearch/byzip")

    zip_code_input = driver.find_element_by_id("SearchTerm")
    zip_code_input.clear()
    zip_code_input.send_keys(zip_input)
    zip_code_input.send_keys(Keys.RETURN)

    while True:
        process_active_companies(driver, cwd)
        if not navigate_to_next_page(driver):
            break

    driver.close()


if __name__ == "__main__":
    main()
