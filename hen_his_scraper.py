#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import argparse
import sys

def main():
    """
    Scrapes web pages and creates a file with expiration dates
    for symbols HEN (Henry Basis Futures) and HIS (Henry Index Futures).
    """
    
    # Create parser.
    parser = argparse.ArgumentParser()
 
    # Add arguments to the parser.
    parser.add_argument("symbol", choices=['HEN', 'HIS'])
 
    # Parse the arguments.
    args = parser.parse_args()
 
    # Get the arguments value
    if args.symbol == 'HEN':
        product_name = 'Henry Basis Future'
        file_name = 'hen_expiry.txt'
        url = 'https://www.theice.com/products/6590136/Henry-Basis-Future/expiry'
    elif args.symbol == 'HIS':
        product_name = 'Henry Index Future'
        file_name = 'his_expiry.txt'
        url = 'https://www.theice.com/products/6590185/Henry-Index-Future/expiry'
    else:
        parser.print_help()
        sys.exit(1)

    # Disable the logging popup.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.minimize_window()
    #driver.maximize_window()

    driver.implicitly_wait(30)  # Seconds.

    # Open web page.
    driver.get(url)

    wait_time = 3   # Seconds.
    #time.sleep(wait_time)

    # The accept cookies policy button.
    wait = WebDriverWait(driver, wait_time)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()

    element = driver.find_element(By.TAG_NAME, 'h2')
   
    print(element.text)

    if element.text == product_name:

        f = open(file_name, 'w')
        f.write(element.text + '\n')

        table = driver.find_element(By.CLASS_NAME, 'table-data')
        #table = driver.find_element(By.TAG_NAME, 'table')
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            index = 0
            contract = expiration_date = None
            for cell in row.find_elements(By.TAG_NAME, 'td'):

                # First column (0) is Contract.
                if index == 0:
                    contract = cell.text

                # Last column (7) is Expiration Date.
                if index == 7:
                    expiration_date = cell.text
                    continue
        
                index = index + 1

            # Only print rows with contracts.
            if contract != None:
                print('{}|{}'.format(contract, expiration_date))
                f.write('{}|{}\n'.format(contract, expiration_date))

    # Close the browser window.
    driver.quit()

    f.close()

    #raw_input('Press Enter to continue ...')

if __name__ == '__main__':
    main()

##END##
