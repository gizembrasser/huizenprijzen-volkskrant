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
chrome_options.add_argument("--headless=new")
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


def accept_cookies(driver):
    """Function to accept cookies."""
    try:
        accept_cookies = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        accept_cookies.click()
    except Exception as e:
        print(f"Error clicking accept cookies button: {e}")


def next_page(driver):
    """Go to the next page."""
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__link--next")))
        next_page_url = next_button.get_attribute("href") 
        driver.get(next_page_url)
        return True
    except Exception:
        print("No more pages found or error navigating to the next page.")
        return False


def collect_links(driver, links_file_path):
    """Function to collect all links from the listing pages."""
    all_links = []

    while True:
        try:
            # Find all <li> elements containing the listings
            listings = driver.find_elements(By.CLASS_NAME, "search-list__item--listing")

            # Collect links from the current page
            for listing in listings:
                link_a = listing.find_element(By.CLASS_NAME, "listing-search-item__link--title")
                all_links.append(link_a.get_attribute("href"))
          
            # Check if there's a next page and move to it
            if not next_page(driver):
                break

        except Exception as e:
            print(f"Error collecting links: {e}")
            break

    # Save the collected links
    with open(links_file_path, mode="w") as file:
        for link in all_links:
            file.write(link + "\n")
    
    print(f"Collected {len(all_links)} links and saved to data/{links_file_path}")


def safe_find(driver, by, value, sub_by=None, sub_value=None):
    """Safely find an element and return its text, optionally find sub-elements."""
    try:
        element = wait.until(EC.presence_of_element_located((by, value)))

        # If sub-element is specified, search within the found element
        if sub_by and sub_value:
            sub_element = element.find_element(sub_by, sub_value)
            return sub_element.text
        
        return element.text    
    except Exception:
        return None


def visit_links(driver, links_file_path, csv_file_path):
    """Visit each link and collect details into CSV."""
    with open(links_file_path, mode="r") as file:
        links = [line.strip() for line in file.readlines()]

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Link', 'Huurprijs', 'Locatie', 'm2', 'Kamers', 'Interieur', 'Huurovereenkomst', 'Badkamers', 'Faciliteiten', 'Balkon', 'Tuin', 'Energie label', 'Opslag', 'Parkeren', 'Type parkeerplaats', 'Garage', 'Beschrijving'])

        # Loop through each link and extract details
        for index, link in enumerate(links, start=1):
            try:
                print(f"Visiting link {index}: {link}")
                driver.get(link)
                time.sleep(2)
                
                # Check if the 'More' button is present, and click if so
                try:
                    more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "listing-detail-description__button")))
                    if more_button:
                        more_button.click()
                        time.sleep(1)
                except Exception:
                    pass

                # Use the safe_find helper to get elements or return None
                price = safe_find(driver, By.CLASS_NAME, "listing-detail-summary__price-main")
                location = safe_find(driver, By.CLASS_NAME, "listing-detail-summary__location")
                size = safe_find(driver, By.CLASS_NAME, "illustrated-features__item--surface-area")
                rooms = safe_find(driver, By.CLASS_NAME, "illustrated-features__item--number-of-rooms")
                interior = safe_find(driver, By.CLASS_NAME, "illustrated-features__item--interior")
                rental_type = safe_find(driver, By.CLASS_NAME, "listing-features__description--contract_duration", By.CLASS_NAME, "listing-features__main-description")
                bathrooms = safe_find(driver, By.CLASS_NAME, "listing-features__description--number_of_bathrooms", By.CLASS_NAME, "listing-features__main-description")
                facilities = safe_find(driver, By.CLASS_NAME, "listing-features__description--facilities", By.CLASS_NAME, "listing-features__main-description")
                balcony = safe_find(driver, By.CLASS_NAME, "listing-features__description--balcony", By.CLASS_NAME, "listing-features__main-description")
                garden = safe_find(driver, By.CLASS_NAME, "listing-features__description--garden", By.CLASS_NAME, "listing-features__main-description")
                energy = safe_find(driver, By.XPATH, "//*[contains(@class, 'listing-features__description--energy-label')]", By.CLASS_NAME, "listing-features__main-description")
                storage = safe_find(driver, By.CLASS_NAME, "listing-features__description--storage", By.CLASS_NAME, "listing-features__main-description")
                parking = safe_find(driver, By.CLASS_NAME, "page__details--parking", By.CLASS_NAME, "listing-features__main-description")
                parking_type = safe_find(driver, By.CLASS_NAME, "page__details--parking", By.CLASS_NAME, "listing-features__description--type")
                garage = safe_find(driver, By.CLASS_NAME, "page__details--garage", By.CLASS_NAME, "listing-features__main-description")
                description = safe_find(driver, By.CLASS_NAME, "listing-detail-description__additional")

                writer.writerow([link, price, location, size, rooms, interior, rental_type, bathrooms, facilities, balcony, garden, energy, storage, parking, parking_type, garage, description])

            except Exception as e:
                print(f"Error visiting link: {link}, {e}")
