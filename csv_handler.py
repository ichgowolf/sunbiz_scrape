import os
from csv import DictWriter


def check_for_file(current_working_directory):
    """
    Check if the 'active_companies.csv' file exists in the specified directory,
    and create it with the appropriate headers if it doesn't.

    This function checks if the 'active_companies.csv' file is present in the
    current_working_directory. If it doesn't exist, the function creates the file
    with the specified header_list and returns True. If the file already exists,
    the function returns True without modifying the file.

    :param current_working_directory: The path to the directory where the 'active_companies.csv' file should be.
    :return: True if the file exists or is successfully created, False otherwise.
    """
    file_path = os.path.join(current_working_directory, "active_companies.csv")
    if os.path.isfile(file_path):
        return True
    else:
        header_list = ["Company Name",
                       "Document Number",
                       "FEI/EIN Number",
                       "Date Filed",
                       "Effective Date",
                       "state"]
        with open(file_path, "w", encoding="utf-8") as file:
            writer = DictWriter(file, delimiter=",", fieldnames=header_list)
            writer.writeheader()
            return True


def add_company(current_working_directory, company_data):
    """
    Add a company's data to the 'active_companies.csv' file in the specified directory.

    This function appends a row containing the company_data to the 'active_companies.csv'
    file located in the current_working_directory. The fieldnames for the CSV file
    are derived from the keys of the company_data dictionary.

    :param current_working_directory: The path to the directory where the 'active_companies.csv' file is located.
    :param company_data: A dictionary containing the company's data to be added to the CSV file.
    """
    field_names = list(company_data.keys())
    file_path = os.path.join(current_working_directory, "active_companies.csv")

    with open(file_path, "a") as f:
        writer = DictWriter(f, fieldnames=field_names)
        writer.writerow(company_data)
