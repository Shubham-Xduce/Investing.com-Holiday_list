import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc 

#driver = uc.Chrome(headless=True, use_subprocess=True)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('detach', True)
options.headless = False #remove
options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(options=options)# remove use_subprocess=True,
#time.sleep(20)


def close_popup():
    try:
        popup_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "popupCloseIcon.largeBannerCloser"))
        )
        popup_close_button.click()
        print("Popup closed successfully.")
    except:
        print("Popup not found or already closed.")

def main():
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get('https://in.investing.com/holiday-calendar/')
        
        close_popup()
        
        button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'datePickerToggleBtn'))
        )
        #button2 = driver.find_element(By.ID, 'datePickerToggleBtn')
        button2.click()
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'applyBtn'))
        )
        print("Apply button found and clickable")
        apply_button.click() 
        
    except Exception as e:
        print("An error occurred:", str(e))
        # Add additional debugging information
    #finally:
    #    driver.quit()

        
if __name__ == "__main__":
    main()

"""
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

def close_popup(driver):
    try:
        popup_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "popupCloseIcon.largeBannerCloser"))
        )
        popup_close_button.click()
        print("Popup closed successfully.")
    except:
        print("Popup not found or already closed.")

def mimic_human_behavior(driver):
    # Add delays to mimic human behavior
    time.sleep(random.uniform(1, 3))

    # Simulate scrolling action
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))

    # Simulate moving the mouse to avoid detection
    actions = ActionChains(driver)
    actions.move_by_offset(random.uniform(-100, 100), random.uniform(-100, 100)).perform()

def main():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('detach', True)
        ua = UserAgent()
        options.add_argument(f"user-agent={ua.random}")
        driver = webdriver.Chrome(options=options)

        driver.get('https://in.investing.com/holiday-calendar/')

        close_popup(driver)
        mimic_human_behavior(driver)

        button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'datePickerToggleBtn'))
        )
        button2.click()

        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'applyBtn'))
        )
        print("Apply button found and clickable")
        apply_button.click()

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
"""

""""""



"""
API details
https://in.investing.com/holiday-calendar/Service/getCalendarFilteredData
POST


PAYLOAD 
"""