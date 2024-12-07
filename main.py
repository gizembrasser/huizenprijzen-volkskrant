import os
import argparse
from pararius_scraper import driver, accept_cookies, collect_links, visit_links
from utils.save_html import save_html
from utils.filters import validate_price_filter

data_folder = os.path.join(os.getcwd(), 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)


def main():
    parser = argparse.ArgumentParser(description="Pararius listing collection")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand to collect data from pararius listings
    collect_parser = subparsers.add_parser("collect_listings", help="Collect data from pararius listings and save it to a CSV file.")
    collect_parser.add_argument(
        "--city", type=str, default="nederland",
        help="Specify the city for the Pararius URL. Default is 'nederland'."
    )
    collect_parser.add_argument(
        "--min_price", type=int, default=None,
        help="Specify the minimum price filter for the rental listings."
    )
    collect_parser.add_argument(
        "--max_price", type=int, default=None,
        help="Specify the maximum price filter for the rental listings."
    )
    collect_parser.add_argument(
        "--csv_file_name", type=str, default="pararius_listings.csv",
        help="Specify the name of the CSV file to save the collected data. Default is 'pararius_listings.csv'."
    )

    # Subcommand to locally save the listings as HTML files
    save_html_parser = subparsers.add_parser("save_html", help="Save HTML pages from a CSV file.")
    save_html_parser.add_argument(
        "--csv_file", type=str, required=True,
        help="Path to the CSV file containing the 'Link' column for HTML saving."
    )

    args = parser.parse_args()

    if args.command == "collect_listings":
        # Validate the min and max price values for filtering
        try:
            min_price, max_price = validate_price_filter(args.min_price, args.max_price)
        except ValueError as e:
            print(e)
            return
        
        # Construct the URL with city and price filter
        base_url = f"https://www.pararius.com/apartments/{args.city.lower()}"
        if min_price and max_price:
            base_url += f"/{min_price}-{max_price}"

        links_file_path = os.path.join(data_folder, 'pararius_links.txt')
        csv_file_path = os.path.join(data_folder, args.csv_file_name)

        driver.get(base_url)

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
            
    elif args.command == "save_html":
        save_html(args.csv_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
