# README.md

## Project Title: MindHive Technical Assessment - Scraping, Storing, and Processing v2

### Overview
This project is a full-stack solution for scraping Subway outlet data from the Subway Malaysia website, storing it in a database, geocoding the addresses, and visualizing the data on a map with additional features like catchment areas and chatbot functionality.

### Features
1. **Web Scraping**: Scrapes Subway outlet data (names, addresses, operating hours, Waze links) from https://subway.com.my/find-a-subway.
2. **Database Storage**: Stores scraped data in a relational database.
3. **Geocoding**: Converts addresses into geographical coordinates (latitude, longitude) using a geocoding service.
4. **API Development**: A FastAPI backend serves the outlet data, including geographical coordinates.
5. **Frontend Visualization**: A web application displays the outlets on a map with a 5KM radius catchment area and highlights overlapping catchments.
6. **Chatbot Functionality**: A search box allows users to query the data (e.g., "Which outlets close the latest?" or "How many outlets are in Bangsar?").

---

### Installation and Setup

#### Prerequisites
- Python 3.8 - 3.11 (For this assessment, python v3.12 has been used)
- SQLite (For database storage)
- Google Maps API key (For geocoding)
- HTML, CSS, and JavaScript (For frontend development)
- FastAPI (For building the API backend)

#### Step 1: Set Up the Backend
1. Create and Activate Virtual Environment
   ```bash
   python -m venv clean_env
   ```
   - Windows: Run this command to activate the virtual environment:
     ```bash
     clean_env\Scripts\activate
     ```
   - Mac/Linux: Run this command to activate the virtual environment:
     ```bash
     source clean_env/bin/activate
     ```

2. Install Python Dependencies (Only Required Packages):
   ```bash
   pip install fastapi googlemaps uvicorn geopy selenium webdriver-manager sqlalchemy dotenv
   ```

3. Generate `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

4. Set Up the Database:
   - Create a SQLite database file named `outlets.db`.
   - Open `database.py`, locate the `DATABASE_URL` variable, and update it as follows:
     ```bash
     DATABASE_URL = "sqlite:///outlets.db"
     ```
5. Run the FastAPI Server:
   ```bash
   uvicorn api:app --reload
   ```

#### Step 2: Set Up the Frontend
1. Navigate to the Frontend Directory:
   ```bash
   cd frontend
   ```

#### Step 3: Configure Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
GEOCODING_API_KEY=google_maps_api_key
DATABASE_URL=sqlite:///outlets.db
DEBUG=True
```

#### Step 4: Create the Repository
1. Initialize Git Repository
```bash
cd mindhive-assessment
git init
```
2. Add Files and Commit Changes
```bash
git add .
git commit -m "Initial commit"
```
3. Push to GitHub
```bash
git branch -M main
git remote add origin <repository-URL>
git pull origin main --rebase   # Ensures no conflicts before pushing
git push -u origin main
```
---

## Usage

### Main Script
The `main.py` script integrates all core functionalities, including web scraping, database storage, and geocoding. Running this script will execute the entire process in one go:
```bash
python main.py
```
### Individual Scripts
For more control, you can run each step separately as follows:

#### 1. Web Scraping
To collect Subway outlet data directly from the website:
```bash
python scraper.py
```

#### 2. Database Storage
To store the scraped data in the SQLite database for easy access and management:
```bash
python database.py
```

#### 3. Geocoding
To convert outlet addresses into geographic coordinates using the Google Maps API:
```bash
python geocoder.py
```

#### API Endpoints
- **GET /**: Root endpoint for the API.
- **GET /outlets**: Fetches all outlets from the database.
- **GET /outlets/{outlet_id}**: Fetches a specific outlet by its ID.
- **GET /outlets/search/**: Searches for outlets by name.
- **GET /outlets/nearby/**: Fetches outlets within a specified radius of the user's location.

#### Frontend
- Open the web application in your browser at `http://127.0.0.1:8000`.
- View Subway outlets on the map with 5KM radius catchments.
- Use the search box to query the data.

---




