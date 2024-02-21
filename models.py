from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    addresses = relationship("Address", back_populates="contact")
    phone_numbers = relationship("PhoneNumber", back_populates="contact")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    contact = relationship("Contact", back_populates="addresses")

class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    type = Column(String)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    contact = relationship("Contact", back_populates="phone_numbers")  
    