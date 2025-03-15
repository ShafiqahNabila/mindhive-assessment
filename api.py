from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from geopy.distance import geodesic

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    :return: SQLite connection object.
    """
    conn = sqlite3.connect('outlets.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def fetch_outlets(query: str, params: tuple = ()):
    """
    Fetches outlets from the database based on a query.

    :param query: SQL query to execute.
    :param params: Parameters for the SQL query (default: empty tuple).
    :return: List of dictionaries representing outlets.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    outlets = cursor.fetchall()
    conn.close()
    return [dict(outlet) for outlet in outlets]

def calculate_distance(user_coords, outlet_coords):
    """
    Calculates the distance between two coordinates using geodesic distance.

    :param user_coords: Tuple of (latitude, longitude) for the user's location.
    :param outlet_coords: Tuple of (latitude, longitude) for the outlet's location.
    :return: Distance in kilometers.
    """
    return geodesic(user_coords, outlet_coords).km

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for the API.

    :return: Welcome message.
    """
    return {"message": "Welcome to the Subway Outlets API!"}

# Endpoint to get all outlets
@app.get("/outlets")
def get_all_outlets():
    """
    Fetches all outlets from the database.

    :return: List of all outlets.
    """
    outlets = fetch_outlets("SELECT * FROM outlets")
    return {"outlets": outlets}

# Endpoint to get an outlet by ID
@app.get("/outlets/{outlet_id}")
def get_outlet_by_id(outlet_id: int):
    """
    Fetches a specific outlet by its ID.

    :param outlet_id: ID of the outlet to fetch.
    :return: Details of the requested outlet.
    :raises HTTPException: If the outlet is not found.
    """
    outlets = fetch_outlets("SELECT * FROM outlets WHERE id = ?", (outlet_id,))
    if outlets:
        return {"outlet": outlets[0]}
    else:
        raise HTTPException(status_code=404, detail="Outlet not found")

# Endpoint to search outlets by name
@app.get("/outlets/search/")
def search_outlets_by_name(name: str):
    """
    Searches for outlets by name.

    :param name: Name or partial name of the outlet to search for.
    :return: List of matching outlets.
    """
    outlets = fetch_outlets("SELECT * FROM outlets WHERE name LIKE ?", (f"%{name}%",))
    return {"outlets": outlets}

# Endpoint to get outlets within a radius (in kilometers)
@app.get("/outlets/nearby/")
def get_outlets_nearby(latitude: float, longitude: float, radius: float):
    """
    Fetches outlets within a specified radius of the user's location.

    :param latitude: Latitude of the user's location.
    :param longitude: Longitude of the user's location.
    :param radius: Radius in kilometers to search within.
    :return: List of nearby outlets.
    """
    outlets = fetch_outlets("SELECT * FROM outlets")
    user_coords = (latitude, longitude)
    nearby_outlets = [
        outlet for outlet in outlets
        if calculate_distance(user_coords, (outlet["latitude"], outlet["longitude"])) <= radius
    ]
    return {"nearby_outlets": nearby_outlets}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)