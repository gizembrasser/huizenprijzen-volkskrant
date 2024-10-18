import os
import csv
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-search-engine-choice-screen")

driver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")

driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

wait = WebDriverWait(driver, 10)


def accept_cookies(driver):
    """Function to accept cookies."""
    try:
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies_button.click()
    except Exception as e:
        print(f"Error clicking accept cookies button: {e}")


def next_page(driver):
    """Function to find the next page link, if it exists, and navigate to it."""
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__link--next")))
        next_page_url = next_button.get_attribute("href")
    
        driver.get(next_page_url)
        return True
    except Exception as e:
        print("No more pages found or error navigating to the next page.")
        return False


def collect_links(driver):
    """Function to collect all links from the listing pages."""
    all_links = []

    while True:
        try:
            # Find all <li> elements with the class "search-list__item search-list__item--listing"
            listings = driver.find_elements(By.CLASS_NAME, "search-list__item--listing")

            # Collect links from the current page
            for listing in listings:
                try:
                    link_a = listing.find_element(By.CLASS_NAME, "listing-search-item__link--title")
                    all_links.append(link_a.get_attribute("href"))
                except Exception as e:
                    print(f"Error finding link: {e}")
            
            # Check if there's a next page and move to it
            if not next_page(driver):
                break
        except Exception as e:
            print(f"Error collecting links: {e}")
            break

    return all_links


def safe_find(driver, by, value):
    """Helper function to safely find an element. Returns an empty string if not found."""
    try:
        return driver.find_element(by, value).text
    except Exception:
        return ""


def visit_links(driver, links):
    """Function to visit each link and extract the required details and save them to a CSV file."""
    csv_file_path = os.path.join(os.getcwd(), 'data/apartment_listings.csv')

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Link', 'Huurprijs', 'Locatie', 'm2', 'Huurovereenkomst', 'Beschrijving'])

        # Loop through each link and extract details
        for link in links:
            try:
                driver.get(link)
                time.sleep(2)  # Give the page some time to load

                # Use the safe_find helper to get elements or return empty strings
                price = safe_find(driver, By.CLASS_NAME, "listing-detail-summary__price-main")
                location = safe_find(driver, By.CLASS_NAME, "listing-detail-summary__location")
                size = safe_find(driver, By.CLASS_NAME, "illustrated-features__item--surface-area")
                rental_type = safe_find(driver, By.CLASS_NAME, "listing-features__main-description")

                # Extract description from nested elements
                try:
                    description_div = driver.find_element(By.CLASS_NAME, "listing-detail-description__additional")
                    description_elements = description_div.find_elements(By.XPATH, ".//*")
                    description_text = " ".join([elem.text for elem in description_elements])
                except Exception:
                    description_text = ""

                # Write the row with the extracted details to the CSV file
                writer.writerow([link, price, location, size, rental_type, description_text])

            except Exception as e:
                print(f"Error visiting link: {link}, {e}")


# Main script
driver.get("https://www.pararius.com/apartments/nederland")

accept_cookies(driver)

all_links = collect_links(driver)

visit_links(driver, all_links)

driver.quit()
