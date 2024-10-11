import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Define the base class for the models
Base = declarative_base()

# Define the models
class Customer(Base):
    """description: Table to store customer information."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)

class Boat(Base):
    """description: Table to store information about boats."""
    __tablename__ = 'boats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    length = Column(Float)
    type = Column(String)

class StorageSlot(Base):
    """description: Table to store information about boat storage slots."""
    __tablename__ = 'storage_slots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    size = Column(String)

class Booking(Base):
    """description: Table to store booking information."""
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    boat_id = Column(Integer, ForeignKey('boats.id'), nullable=False)
    storage_slot_id = Column(Integer, ForeignKey('storage_slots.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)

class Service(Base):
    """description: Table to list various services offered."""
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)

class BoatService(Base):
    """description: Table to store service appointments for boats."""
    __tablename__ = 'boat_services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)

class Employee(Base):
    """description: Table to store employee information."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Part(Base):
    """description: Table to store information about parts available for purchase."""
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float)

class Repair(Base):
    """description: Table to store repair records."""
    __tablename__ = 'repairs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    boat_service_id = Column(Integer, ForeignKey('boat_services.id'), nullable=False)
    description = Column(Text)

class Transaction(Base):
    """description: Table to store transactions made by customers."""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)

class Supply(Base):
    """description: Table to store supply details for parts."""
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    supplier_name = Column(String, nullable=False)

class Invoice(Base):
    """description: Table to generate invoice records."""
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    issue_date = Column(DateTime, default=datetime.datetime.utcnow)

# Setup database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data to populate the tables
customers = [
    Customer(name='John Doe', email='john.doe@example.com'),
    Customer(name='Jane Smith', email='jane.smith@example.com')
]

boats = [
    Boat(name='Aqua Voyager', length=30.5, type='Sailboat'),
    Boat(name='Sea Explorer', length=25.0, type='Motorboat')
]

storage_slots = [
    StorageSlot(location='A1', size='Large'),
    StorageSlot(location='B2', size='Medium')
]

bookings = [
    Booking(customer_id=1, boat_id=1, storage_slot_id=1, start_date=datetime.datetime(2023, 11, 15)),
    Booking(customer_id=2, boat_id=2, storage_slot_id=2, start_date=datetime.datetime(2023, 12, 1))
]

services = [
    Service(name='Cleaning', description='Boat cleaning services'),
    Service(name='Winterization', description='Prepare boats for winter storage'),
    Service(name='Repair', description='Engine repair services')
]

boat_services = [
    BoatService(booking_id=1, service_id=1, scheduled_date=datetime.datetime(2023, 11, 16)),
    BoatService(booking_id=2, service_id=2, scheduled_date=datetime.datetime(2023, 12, 2))
]

employees = [
    Employee(name='Alice Johnson', role='Technician'),
    Employee(name='Bob Brown', role='Manager')
]

parts = [
    Part(name='Propeller', price=300.0),
    Part(name='Engine Oil', price=25.0)
]

repairs = [
    Repair(boat_service_id=1, description='Replaced engine oil filter'),
    Repair(boat_service_id=2, description='Fixed propeller alignment')
]

transactions = [
    Transaction(customer_id=1, amount=329.99),
    Transaction(customer_id=2, amount=850.00)
]

supplies = [
    Supply(part_id=1, supplier_name='Marine Supplies Inc.'),
    Supply(part_id=2, supplier_name='Boat Tech Co.')
]

invoices = [
    Invoice(transaction_id=1),
    Invoice(transaction_id=2)
]

# Add data to session and commit
session.add_all(customers + boats + storage_slots + bookings + services + 
                boat_services + employees + parts + repairs + transactions + supplies + invoices)
session.commit()

# Close the session
session.close()
