import requests
import pandas as pd
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def save_html(csv_file):
    """Function that takes a CSV file as argument, reads the column containing URLs, and saves the HTML files for local access."""
    df = pd.read_csv(csv_file)

    for idx, url in enumerate(df["Link"]):
        try:
            # Send a GET request to retrieve the webpage
            response = requests.get(url, verify=False)
            response.raise_for_status()

            # Parse the HTML with BeautifulSoup to check for specific content
            soup = BeautifulSoup(response.text, 'html.parser')
            notification_element = soup.find("div", class_="notification__title")

            # If the notification element is found, skip saving the HTML file
            if notification_element and notification_element.get_text(strip=True) == "Not available":
                print(f"Skipped link {idx + 1}: {url} (Page unavailable)")
                continue

            # Extract the last segment of the URL path for naming the file
            url_path = urlparse(url).path.strip('/').split('/')
            filename = f"{url_path[-2]}_{url_path[-1]}.html"

            # Save the webpage content as an HTML file
            with open(f"../data/html/{filename}", mode="w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"Saved link {idx + 1}: {url} as {filename}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")


# save_html("../data/pararius_listings02112024.csv")
