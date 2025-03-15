from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Initialize and return the Selenium WebDriver."""
    return webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

def search_city(driver, city):
    """Enter the city name into the search box and click the search button."""
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fp_searchAddress"))
        )
        search_box.send_keys(city)

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "fp_searchAddressBtn"))
        )
        search_button.click()
        time.sleep(5)  # Wait for results to load
    except Exception as e:
        print(f"Error filtering by city: {e}")

def scroll_to_bottom(driver):
    """Scroll to the bottom of the page to load all outlets."""
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_outlet_details(container):
    """Extract and return outlet details from a container."""
    try:
        name_element = container.find_element(By.TAG_NAME, "h4")
        name = name_element.text.strip() if name_element else "Not available"

        address_element = container.find_element(By.CLASS_NAME, "infoboxcontent").find_element(By.TAG_NAME, "p")
        address = address_element.text.strip() if address_element else "Not available"

        operating_hours_elements = container.find_element(By.CLASS_NAME, "infoboxcontent").find_elements(By.TAG_NAME, "p")
        operating_hours = operating_hours_elements[2].text.strip() if len(operating_hours_elements) > 2 else "Not available"

        waze_link_element = container.find_element(By.CLASS_NAME, "infoboxlink").find_element(By.TAG_NAME, "a")
        waze_link = waze_link_element.get_attribute("href") if waze_link_element else "Not available"

        if name != "Not available" and address != "Not available":
            return {
                "name": name,
                "address": address,
                "operating_hours": operating_hours,
                "waze_link": waze_link
            }
    except Exception as e:
        print(f"Error parsing outlet: {e}")
    return None

def scrape_subway_outlets_selenium(base_url, city="kuala lumpur"):
    """
    Scrapes Subway outlets using Selenium for dynamic content.
    
    :param base_url: The base URL to scrape (e.g., https://subway.com.my/find-a-subway)
    :param city: The city to filter by (default: kuala lumpur)
    :return: A list of dictionaries containing outlet details.
    """
    outlets = []
    driver = setup_driver()
    driver.get(base_url)

    search_city(driver, city)
    scroll_to_bottom(driver)

    outlet_containers = driver.find_elements(By.CLASS_NAME, "fp_listitem")
    for container in outlet_containers:
        outlet_details = extract_outlet_details(container)
        if outlet_details:
            outlets.append(outlet_details)

    driver.quit()
    return outlets