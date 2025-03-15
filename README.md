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
- Python 3.8 - 3.11 (For this assessment, python version 3.12 has been used)
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

### Main 
Containing main function from scraping, storing, and geocoding, can use to complete the function in one go:
```bash
python main.py
```

#### Web Scraping
Run the scraping script only to collect data from the Subway website:
```bash
python scraper.py
```

#### Database Storing
Store the scraped data in the database:
```bash
python database.py
```

#### Geocoding
Run the geocoding script to convert addresses into coordinates:
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

### Project Structure
```
subway-finder/
├── main/ 
├── database/ 
├── geocoder/ 
├── models
├── api/ 
├── scraper/ 
├── outlets/                                  
├── frontend/                 
│   ├── index/               
│   ├── script/                  
│   └── style/                      
├── .venv                     # Environment variables (virtual environment)
├── DOCUMENTATION.md          # Project documentation        
└── README.md                 # Project explanation

```

---

### Key Technical Decisions
1. **Web Scraping**: Used `BeautifulSoup` and `requests` for scraping due to their simplicity and effectiveness.
2. **Database**: Chose PostgreSQL for its robustness and scalability.
3. **Geocoding**: Used Google Maps API for accurate geocoding.
4. **Backend**: FastAPI was chosen for its speed, modern features, and automatic OpenAPI documentation.
5. **Frontend**: React with `react-leaflet` for map visualization due to its flexibility and ease of use.
6. **Chatbot**: Implemented a simple search functionality using regex and NLP techniques for query handling.

---

### Troubleshooting
- **Database Connection Issues**: Ensure the database is running and the connection string in `config.py` is correct.
- **Geocoding Failures**: Verify that the Google Maps API key is valid and has sufficient quota.
- **Frontend Not Loading**: Ensure the backend server is running and the frontend is correctly configured to communicate with it.

---

### Future Improvements
- Add caching for geocoding requests to reduce API calls.
- Implement user authentication for the API.
- Enhance the chatbot with more advanced NLP models (e.g., GPT-based models).

---




