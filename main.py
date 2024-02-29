"""
This script scrap holiday calendar data from a webpage and loads it into database table.

it uses Selenium for web scraping and pyodbc for database interaction.
arguments for configuratiom, such as enabling debug mode, specifying the SQL server section name,
setting the path to the Chrome webdriver, and providing the URL of the webpage to scrape.

Dependencies
- Selenium: for web scraping

Usage:
python market_holiday.py [--debug] [--sqlSectionName SQL_SECTION_NAME] [--chromeDriverPath CHROME_DRIVER_NAME] [--url URL]

@author- Abhishek Tiwari
"""
import os
import time
import logging
import sys
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from SEG.DB.DBConn import DBConn as db_util

# def process_local_variables():
#     """
#     Process command line arguments and return a dictionary of parameters.

#     Returns:
#         dict: Dictionary containing processed parameters.
#     """
#     parser = argparse.ArgumentParser("Test Locations - send email to users about bank fail notify")
#     parser.add_argument('--debug', help="Put the logging module into debug mode", action="store_true")
#     parser.add_argument('--sqlSectionName', help="Name of section in sql ini file", dest="sqlSectionName", default=os.environ.get("PYODBC_SERVER"))
#     parser.add_argument('--chromeDriverPath',help="Path of your chromedriver", default=os.environ.get("CHROME_DRIVER_PATH"))
#     parser.add_argument('--url', help="Url Link", default="https://in.investing.com/holiday-calendar/")
#     args = parser.parse_args()
#     param_variables = {}
#     param_variables["debug"] = args.debug
#     param_variables["sqlSectionName"] = args.sqlSectionName
#     param_variables["url"] = args.url
#     param_variables["chromeDriverPath"] = args.chromeDriverPath

#     return param_variables

def setup_webdriver(chrome_driver_path):
    """
    Set up and return a headless Chrome webdriver.

    Args:
        chrome_driver_path (str): Path to the Chrome driver executable.

    Returns:
        webdriver.Chrome: Configured Chrome webdriver.
    """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--webdriver-path={chrome_driver_path}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=chrome_options)

def find_element_with_retry(driver, by, value, max_retries=3):
    """
    Find an HTML element with retry mechanism.

    Args:
        driver (webdriver): Selenium webdriver.
        by (selenium.webdriver.common.by.By): Locator strategy.
        value (str): Locator value.
        max_retries (int): Maximum number of retries.

    Returns:
        WebElement: Found HTML element.

    Raises:
        NoSuchElementException: If element is not found after maximum retries.
    """
    for _ in range(max_retries):
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            logging.warning(f"Element not found. Retrying...")
            time.sleep(2)
    raise NoSuchElementException(f"Element not found after {max_retries} retries")

def scrape_data(driver, url, table_id, db_conn):
    """
    Scrape data from a table on a webpage.

    Args:
        driver (webdriver): Selenium webdriver.
        url (str): URL of the webpage.
        table_id (str): ID of the HTML table to scrape.
        db_conn (pyodbc.Connection): Database connection object.

    Returns:
        list: List of tuples containing scraped data.
    """
    driver.get(url)
    
    # Wait for the table to be present before extracting data
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))
    except TimeoutException:
        logging.error("Timed out waiting for the table to be present.")
        sys.exit(-1)

    table_element = find_element_with_retry(driver, By.ID, table_id)
    table_data = []
    previous_date = None
    rows = table_element.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        if columns and "Early" not in columns[3].text:
            date_str = columns[0].text.strip()
            try:
                date = datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")
                previous_date = date
            except Exception as e:
                date = previous_date
            country = columns[1].text
            exchange = columns[2].text
            holiday = columns[3].text.replace("'", "-")
            comment = "https://in.investing.com/holiday-calendar/"

            # Fetch ISO code from the database based on the exchange name
            iso_code = get_iso_code(db_conn, exchange)

            if iso_code:
                data = (date, country, iso_code, exchange, holiday, comment)
                table_data.append(data)
            else:
                logging.warning(f"ISO code not found for exchange: {country}")

    return table_data

def get_iso_code(db_conn, exchange):
    """
    Fetch ISO code from the database based on the exchange name.

    Args:
        db_conn (pyodbc.Connection): Database connection object.
        exchange_name (str): Name of the exchange.

    Returns:
        str: ISO code of the country associated with the exchange.
    """
    
    try:
        cursor = db_conn.cursor()
        
        query = f"SELECT Country_ISO_Code from  [BloombergMarketData].[dbo].[Market_Holidays] where Exchange_Name = '{exchange.strip()}'"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            iso_code = row[0]
            return iso_code
        else:
            return None
    except Exception as e:
        logging.error(f"Error fetching ISO code for exchange {exchange}: {str(e)}")
        return None
    finally:
        cursor.close()

def get_db_connection(conn):
    """
    Establish a connection to the database.

    Args:
        conn (str): Name of the database connection section.

    Returns:
        pyodbc.Connection: Database connection object.
    """
    try:
        logging.info("Starting to connect with the database")
        db_conn = db_util().get_connection(conn)
        logging.info("Connection stabilized with the database")
        return db_conn

    except Exception as e:
        logging.error("Error in database connection: %s", str(e))
        sys.exit(-1)

def load_data_into_database(db_conn, data):
    """
    Load data into the database using MERGE statement for upsert.

    Args:
        db_conn (pyodbc.Connection): Database connection object.
        data (list): List of tuples containing data to be inserted or updated.
    """
    if db_conn:
        cursor = db_conn.cursor()
        cursor.fast_executemany = True
        try:
            placeholders = ",".join(["(?, ?, ?, ?, ?, ?)"] * len(data))
            query = """
                MERGE INTO [BloombergMarketData].[dbo].[Market_Holidays] AS target
                USING (
                    VALUES {}
                ) AS source (Date, Country, Country_ISO_Code, Exchange_Name, Holiday, Comments)
                ON (target.Date = source.Date AND target.Exchange_Name = source.Exchange_Name) 
                WHEN NOT MATCHED THEN
                    INSERT (Date, Country, Country_ISO_Code, Exchange_Name, Holiday, Comments)
                    VALUES (source.Date, source.Country, source.Country_ISO_Code, source.Exchange_Name, source.Holiday, source.Comments);
            """.format(placeholders)
            flattened_data = [item for sublist in data for item in sublist]  # Flatten the data list
            logging.debug(f"QUERY TO execute: {query}")
            cursor.execute(query, flattened_data)  # Pass flattened data to cursor.execute

            db_conn.commit()
            cursor.close()
            logging.info("Data successfully inserted or updated in [BloombergMarketData].[dbo].[Market_Holidays]")

        except Exception as e:
            logging.error("Error in database execute: %s", str(e))
            sys.exit(-1)

def main():
    """
    Main function to execute the data scraping and loading process.
    """
    # Configure logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Process command line arguments
    param_variables = process_local_variables()

    # Set up the Chrome webdriver
    chrome_driver_path = param_variables["chromeDriverPath"]
    driver = setup_webdriver(chrome_driver_path)

    try:
        # Establish a connection to the database
        db_conn = get_db_connection(param_variables["sqlSectionName"])

        # Scrape data from the webpage
        url = param_variables["url"]
        table_id = "holiday_div"
        table_data = scrape_data(driver, url, table_id, db_conn)

    finally:
        driver.quit()

    # Load data into the database
    load_data_into_database(db_conn, table_data)

if __name__ == "__main__":
    main()