import os
from pararius_scraper import driver, accept_cookies, collect_links, visit_links

data_folder = os.path.join(os.getcwd(), 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

links_file_path = os.path.join(data_folder, 'pararius_links.txt')
csv_file_path = os.path.join(data_folder, 'pararius_listings.csv')

driver.get("https://www.pararius.com/apartments/nederland")

accept_cookies(driver)

# Check if the links file already exists
if not os.path.exists(links_file_path):
    print(f"{links_file_path} not found, collecting links...")
    collect_links(driver, links_file_path)
else:
    print(f"{links_file_path} already exists, skipping link collection.")

# Visiting links and saving details to CSV
visit_links(driver, links_file_path, csv_file_path)

print("Finished collecting data.")

driver.quit()