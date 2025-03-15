## Part 6: Documentation and Instructions

### **1. Introduction**
This document provides comprehensive instructions for setting up, understanding, and utilizing the solution for the Subway outlets assessment project. It includes technical decisions, framework choices, and guidance for maintaining the project effectively.

---

### **2. Project Overview**
This project leverages FastAPI as the backend framework and SQLite for database storage. It integrates web scraping, geocoding, and data visualization to present Subway outlets on an interactive map with a 5KM radius feature. The solution is designed to ensure efficiency, scalability, and maintainability.

---

### **3. Setup Instructions**

#### **Step 1: Prerequisites**
Ensure the following tools are installed:
- **Python 3.8 - 3.11** 
- **SQLite** for database management
- **Google Maps API Key** for geocoding services

---

#### **Step 2: Backend Setup**
1. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv clean_env
   clean_env\Scripts\activate  # Windows
   source clean_env/bin/activate # Mac/Linux
   ```

2. **Install Essential Dependencies**
   ```bash
   pip install fastapi uvicorn sqlite geopy requests googlemaps sqlalchemy dotenv
   ```

3. **Database Configuration**
   - Create a SQLite database named `outlets.db` in the project folder.
   - In `database.py`, locate the `DATABASE_URL` variable and ensure it points to:
     ```python
     DATABASE_URL = "sqlite:///outlets.db"
     ```

4. **Run the FastAPI Server**
   ```bash
   uvicorn api:app --reload
   ```

---

#### **Step 3: Frontend Setup**
1. **Navigate to the Frontend Directory**
   ```bash
   cd frontend
   ```


---

#### **Step 4: Environment Variables**
Create a `.env` file in the root folder with the following entries:
```env
DATABASE_URL=sqlite:///outlets.db
GOOGLE_MAPS_API_KEY=API_KEY_HERE
```

---

### **4. Technical Decisions**

#### **Framework Choice: FastAPI**
- **Reasoning:** FastAPI was selected as the backend framework due to its modern, asynchronous capabilities, which make it ideal for handling multiple concurrent requests. Since this project involves web scraping, data storage, and API requests, FastAPI’s non-blocking I/O operations significantly improve efficiency. FastAPI’s automatic OpenAPI documentation simplifies testing, debugging, and potential future integrations. Compared to traditional frameworks like Flask or Django, FastAPI’s lightweight design and impressive performance make it the best choice for this project’s requirements.

#### **Database Choice: SQLite**
- **Reasoning:** SQLite was chosen as the database solution for its simplicity, portability, and minimal configuration requirements. Since the project involves managing a moderate-sized dataset containing Subway outlet details, SQLite’s lightweight structure was sufficient. Its serverless architecture eliminates the need for complex setup, ensuring faster deployment. While PostgreSQL offers advanced features like enhanced indexing, scalability, and concurrent write support, SQLite was preferred because the project’s dataset size and functionality requirements did not justify the overhead of PostgreSQL. If the project expands significantly in the future, migrating to PostgreSQL may become a viable option.

#### **Geocoding Service: Google Maps API**
- **Reasoning:** The Google Maps API was selected for geocoding due to its exceptional accuracy, extensive global coverage, and seamless integration features. Since precise address-to-coordinate conversion was crucial for mapping Subway outlet locations, Google Maps API provided reliable results. While OpenStreetMap’s Nominatim service offers a free alternative, Google Maps API was preferred for its superior accuracy in urban areas, where Subway outlets are typically located. Additionally, Google Maps API’s structured pricing model ensures consistent performance without unexpected rate limits, making it a stable and scalable choice for this project’s needs.

#### **Web Scraping Tools: Selenium & WebDriver**
- **Reasoning:** Initially, web scraping was attempted using requests and BeautifulSoup. However, since the Subway website loads content dynamically using JavaScript, these tools struggled to extract the complete dataset. Consequently, Selenium with WebDriver was chosen for its ability to handle interactive and JavaScript-driven content. Selenium's automation features allowed for effective navigation through the website’s dynamic structure, ensuring all necessary data was collected accurately. Its versatility in interacting with web elements, combined with robust support for multiple browsers, made Selenium the optimal choice for this project’s scraping requirements.


---

### **5. Usage Instructions**

#### Main Script
The `main.py` script integrates all core functionalities, including web scraping, database storage, and geocoding. Running this script will execute the entire process in one go:
```bash
python main.py
```
#### Individual Scripts
For more control, you can run each step separately as follows:

##### 1. Web Scraping
To collect Subway outlet data directly from the website:
```bash
python scraper.py
```

##### 2. Database Storage
To store the scraped data in the SQLite database for easy access and management:
```bash
python database.py
```

##### 3. Geocoding
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

### **6. Troubleshooting Tips**
- **Dependency Issues:** Run `pip install -r requirements.txt` if essential dependencies are missing.
- **API Key Errors:** Ensure your `.env` file is correctly configured.
- **Database Errors:** Confirm `outlets.db` exists and the `DATABASE_URL` is correctly assigned.

---

### **7. Best Practices**
- Regularly update your dependencies to avoid compatibility issues.
- Follow PEP 8 standards to maintain clean and consistent code.
- Document new features or changes to simplify future updates.

---

### **8. Future Enhancements**
- Introduce pagination for large data retrieval.
- Add user authentication for enhanced security.
- Integrate automated tests to improve code reliability.

---

### **9. Contact and Support**
For further guidance or technical support, please reach out to me or refer to the project's GitHub repository.

