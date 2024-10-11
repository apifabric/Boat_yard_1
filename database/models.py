# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 11, 2024 20:09:38
# Database: sqlite:////tmp/tmp.Htu8qD7Gw3/Boat_yard_1/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Boat(SAFRSBaseX, Base):
    """
    description: Table to store information about boats.
    """
    __tablename__ = 'boats'
    _s_collection_name = 'Boat'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    length = Column(Float)
    type = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="boat")



class Customer(SAFRSBaseX, Base):
    """
    description: Table to store customer information.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="customer")
    TransactionList : Mapped[List["Transaction"]] = relationship(back_populates="customer")



class Employee(SAFRSBaseX, Base):
    """
    description: Table to store employee information.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)



class Part(SAFRSBaseX, Base):
    """
    description: Table to store information about parts available for purchase.
    """
    __tablename__ = 'parts'
    _s_collection_name = 'Part'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    SupplyList : Mapped[List["Supply"]] = relationship(back_populates="part")



class Service(SAFRSBaseX, Base):
    """
    description: Table to list various services offered.
    """
    __tablename__ = 'services'
    _s_collection_name = 'Service'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    BoatServiceList : Mapped[List["BoatService"]] = relationship(back_populates="service")



class StorageSlot(SAFRSBaseX, Base):
    """
    description: Table to store information about boat storage slots.
    """
    __tablename__ = 'storage_slots'
    _s_collection_name = 'StorageSlot'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    size = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="storage_slot")



class Booking(SAFRSBaseX, Base):
    """
    description: Table to store booking information.
    """
    __tablename__ = 'bookings'
    _s_collection_name = 'Booking'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    boat_id = Column(ForeignKey('boats.id'), nullable=False)
    storage_slot_id = Column(ForeignKey('storage_slots.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)

    # parent relationships (access parent)
    boat : Mapped["Boat"] = relationship(back_populates=("BookingList"))
    customer : Mapped["Customer"] = relationship(back_populates=("BookingList"))
    storage_slot : Mapped["StorageSlot"] = relationship(back_populates=("BookingList"))

    # child relationships (access children)
    BoatServiceList : Mapped[List["BoatService"]] = relationship(back_populates="booking")



class Supply(SAFRSBaseX, Base):
    """
    description: Table to store supply details for parts.
    """
    __tablename__ = 'supplies'
    _s_collection_name = 'Supply'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    part_id = Column(ForeignKey('parts.id'), nullable=False)
    supplier_name = Column(String, nullable=False)

    # parent relationships (access parent)
    part : Mapped["Part"] = relationship(back_populates=("SupplyList"))

    # child relationships (access children)



class Transaction(SAFRSBaseX, Base):
    """
    description: Table to store transactions made by customers.
    """
    __tablename__ = 'transactions'
    _s_collection_name = 'Transaction'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("TransactionList"))

    # child relationships (access children)
    InvoiceList : Mapped[List["Invoice"]] = relationship(back_populates="transaction")



class BoatService(SAFRSBaseX, Base):
    """
    description: Table to store service appointments for boats.
    """
    __tablename__ = 'boat_services'
    _s_collection_name = 'BoatService'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    booking_id = Column(ForeignKey('bookings.id'), nullable=False)
    service_id = Column(ForeignKey('services.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    booking : Mapped["Booking"] = relationship(back_populates=("BoatServiceList"))
    service : Mapped["Service"] = relationship(back_populates=("BoatServiceList"))

    # child relationships (access children)
    RepairList : Mapped[List["Repair"]] = relationship(back_populates="boat_service")



class Invoice(SAFRSBaseX, Base):
    """
    description: Table to generate invoice records.
    """
    __tablename__ = 'invoices'
    _s_collection_name = 'Invoice'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(ForeignKey('transactions.id'), nullable=False)
    issue_date = Column(DateTime)

    # parent relationships (access parent)
    transaction : Mapped["Transaction"] = relationship(back_populates=("InvoiceList"))

    # child relationships (access children)



class Repair(SAFRSBaseX, Base):
    """
    description: Table to store repair records.
    """
    __tablename__ = 'repairs'
    _s_collection_name = 'Repair'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    boat_service_id = Column(ForeignKey('boat_services.id'), nullable=False)
    description = Column(Text)

    # parent relationships (access parent)
    boat_service : Mapped["BoatService"] = relationship(back_populates=("RepairList"))

    # child relationships (access children)
