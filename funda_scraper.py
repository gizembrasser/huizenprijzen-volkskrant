import os
import csv
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-search-engine-choice-screen")

# Disable SSL verification in Selenium Wire
seleniumwire_options = {'verify_ssl': False}

driver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")

driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=chrome_options,
#     seleniumwire_options=seleniumwire_options
# )

wait = WebDriverWait(driver, 10)

driver.get("https://www.funda.nl/zoeken/huur/?selected_area=%5B%22nl%22%5D")

driver.quit()