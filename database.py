from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Outlet

# Database configuration
DATABASE_URL = "sqlite:///outlets.db"  
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    """
    Creates the database and tables if they don't already exist.
    """
    try:
        Base.metadata.create_all(engine)
        print("Database and tables created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

def save_outlets(outlets, db_url=DATABASE_URL):
    """
    Saves scraped outlets to the database.

    :param outlets: A list of dictionaries containing outlet details.
    :param db_url: Database URL (default: SQLite 'outlets.db').
    """
    try:
        # Create a new session
        session = Session()

        # Add each outlet to the session
        for outlet_data in outlets:
            outlet = Outlet(
                name=outlet_data["name"],
                address=outlet_data["address"],
                operating_hours=outlet_data["operating_hours"],
                waze_link=outlet_data["waze_link"]
            )
            session.add(outlet)

        # Commit the session to save changes
        session.commit()
        print(f"Successfully saved {len(outlets)} outlets to the database.")
    except Exception as e:
        print(f"Error saving outlets to the database: {e}")
    finally:
        # Ensure the session is closed
        session.close()

def main():
    """
    Example usage of the database functions.
    """
    # Example outlets data
    outlets = [
        {
            "name": "Subway Outlet 1",
            "address": "123 Main Street",
            "operating_hours": "9 AM - 9 PM",
            "waze_link": "https://waze.com/..."
        },
        {
            "name": "Subway Outlet 2",
            "address": "456 Elm Street",
            "operating_hours": "10 AM - 8 PM",
            "waze_link": "https://waze.com/..."
        }
    ]

    # Step 1: Create the database
    create_database()

    # Step 2: Save outlets to the database
    save_outlets(outlets)

if __name__ == "__main__":
    main()