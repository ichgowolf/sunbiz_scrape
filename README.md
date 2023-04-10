**Sunbiz Corporation Scraper**

This Python script scrapes the Sunbiz website to gather information about active companies in a specific zip code.

**Dependencies**

Python 3.6+

Selenium

BeautifulSoup


**Installation**
1. Clone this repository or download the files to your local machine.

2. Create a virtual environment and activate it:

```
python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate  # Windows
```

3. Install the required dependencies using pip:
```
pip install -r requirements.txt
```
4. Download the appropriate ChromeDriver for your system and place it in the same directory as the script.

**Usage**

1. Run the main.py script using Python:
```
python main.py
```
2. Enter the desired Floridian zip code when prompted:
```
Enter zip code: 33157
```

The script will navigate through the search results and gather information about the active companies. It will then create a CSV file named active_companies.csv in the script's directory, with the following columns:

Company Name

Document Number

FEI/EIN Number

Date Filed

Effective Date

State

