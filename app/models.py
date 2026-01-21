from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Table
from datetime import date
from app.extensions import db




class Base(DeclarativeBase):
    pass

service_mechanic = Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_id', ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    vehicles = relationship('Vehicle', back_populates='owner')

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, ForeignKey('customers.id'))
    owner = relationship('Customer', back_populates='vehicles')

    services = relationship('ServiceTicket', back_populates='vehicle')


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    service_date = db.Column(db.Date, default=date.today)
    cost = db.Column(db.Float)

    vehicle_id = db.Column(db.Integer, ForeignKey('vehicles.id'))
    vehicle = relationship('Vehicle', back_populates='services')

    mechanics = relationship(
        'Mechanic',
        secondary=service_mechanic,
        back_populates='services'
    )

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    salary = db.Column(db.Float)

    services = relationship(
        'ServiceTicket',
        secondary=service_mechanic,
        back_populates='mechanics'
    )
