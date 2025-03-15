from scraper import scrape_subway_outlets_selenium
from database import create_database, save_outlets
from geocoder import geocode_outlets
import sqlite3

def delete_blank_rows(outlets):
    """
    Filters out entries where the name or address is blank before saving to the database.
    
    :param outlets: List of outlet dictionaries.
    :return: Cleaned list of outlets.
    """
    return [outlet for outlet in outlets if outlet['name'] and outlet['address']]

def scrape_and_save_outlets(base_url, db_path='outlets.db'):
    """
    Scrapes Subway outlets, cleans the data, and saves it to the database.

    :param base_url: The base URL to scrape.
    :param db_path: Path to the SQLite database (default: 'outlets.db').
    :return: List of cleaned outlets.
    """
    # Step 1: Scrape data
    outlets = scrape_subway_outlets_selenium(base_url)

    # Step 2: Clean the data by removing blank rows
    cleaned_outlets = delete_blank_rows(outlets)

    # Step 3: Create the database and tables
    create_database()

    # Step 4: Save cleaned data to the database
    save_outlets(cleaned_outlets, db_path)

    return cleaned_outlets

def main():
    # Configuration
    base_url = "https://subway.com.my/find-a-subway"
    db_path = 'outlets.db'

    # Step 1: Scrape and save outlets
    outlets = scrape_and_save_outlets(base_url, db_path)

    # Step 2: Geocode addresses
    geocode_outlets(db_path)

    print(f"Scraped, saved, and geocoded {len(outlets)} outlets to the database.")

if __name__ == "__main__":
    main()
