from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Table
from datetime import date
from app.extensions import db

service_inventory = db.Table(
    'service_inventory',
    db.Column('service_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True)
)

service_mechanic = db.Table(
    'service_mechanic',
    db.Column('service_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    password = db.Column(db.String(255), nullable=False)

    vehicles = relationship('Vehicle', back_populates='owner')

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), unique=True, nullable=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, ForeignKey('customers.id'))
    owner = relationship('Customer', back_populates='vehicles')

    services = relationship('ServiceTicket', back_populates='vehicle')


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    service_date = db.Column(db.Date, default=date.today)
    cost = db.Column(db.Float)

    vehicle_id = db.Column(db.Integer, ForeignKey('vehicles.id'))
    vehicle = relationship('Vehicle', back_populates='services')

    inventory = relationship(
        'Inventory',
        secondary=service_inventory,
        back_populates='services'
    )

    mechanics = relationship(
        'Mechanic',
        secondary=service_mechanic,
        back_populates='services'
    )

class Mechanic(db.Model):
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

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    services = relationship(
        'ServiceTicket',
        secondary=service_inventory,
        back_populates='inventory'
    )