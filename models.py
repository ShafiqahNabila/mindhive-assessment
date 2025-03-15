from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Define the database schema
Base = declarative_base()

class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    operating_hours = Column(String, nullable=False)
    waze_link = Column(String, nullable=False)
    latitude = Column(Float)  # Will be added later for geocoding
    longitude = Column(Float)  # Will be added later for geocoding