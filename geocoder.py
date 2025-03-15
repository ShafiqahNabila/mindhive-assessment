import googlemaps
import sqlite3
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def geocode_with_google(address):
    """
    Geocodes an address using Google Maps API.
    """
    api_key = os.getenv("GEOCODING_API_KEY")
    if not api_key:
        print("Error: API key is missing. Check your .env file.")
        return None

    gmaps = googlemaps.Client(key=api_key)
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            print(f"No results found for address: {address}")
            return None
    except googlemaps.exceptions.ApiError as e:
        print(f"Google Maps API error: {e}")
    except googlemaps.exceptions.TransportError as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error geocoding with Google Maps: {e}")
    return None

def fetch_outlets_to_geocode(db_path):
    """
    Fetches outlets from the database that need geocoding.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, address FROM outlets WHERE latitude IS NULL OR longitude IS NULL")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def update_outlet_coordinates(outlet_id, latitude, longitude, db_path):
    """
    Updates the latitude and longitude of an outlet in the database.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE outlets SET latitude = ?, longitude = ? WHERE id = ?",
                (latitude, longitude, outlet_id)
            )
            conn.commit()
            print(f"Updated outlet {outlet_id} with coordinates: ({latitude}, {longitude})")
    except sqlite3.Error as e:
        print(f"Database update error for outlet {outlet_id}: {e}")

def geocode_outlets(db_path, retries=3, retry_delay=2):
    """
    Retrieves latitude and longitude for each outlet using Google Maps API.
    """
    outlets = fetch_outlets_to_geocode(db_path)
    if not outlets:
        print("No outlets to geocode. All addresses already have coordinates.")
        return

    for outlet_id, address in outlets:
        for attempt in range(retries):
            print(f"Geocoding outlet {outlet_id}: {address} (Attempt {attempt + 1})")
            coordinates = geocode_with_google(address)
            if coordinates:
                latitude, longitude = coordinates
                update_outlet_coordinates(outlet_id, latitude, longitude, db_path)
                break  # Exit retry loop if successful
            else:
                print(f"Could not geocode address: {address}")
                break
            if attempt < retries - 1:
                time.sleep(retry_delay)

def main():
    """
    Main function to execute the geocoding process.
    """
    db_path = 'outlets.db'

    print("Starting geocoding process...")
    geocode_outlets(db_path)
    print("Geocoding process completed.")

if __name__ == "__main__":
    main()
