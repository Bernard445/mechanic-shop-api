# Building API with Application Factory Pattern

This project is a Flask REST API for a mechanic shop built using the
Application Factory Pattern. It uses SQLAlchemy for database models,
Marshmallow for serialization and validation, and Blueprints for
organizing routes.

## Features

- Application Factory Pattern
- Blueprint-based routing
- SQLAlchemy ORM
- Marshmallow schemas
- MySQL database integration
- CRUD operations for Mechanics
- CRUD operations for Customers
- Vehicles linked to Customers
- Service Tickets linked to Vehicles
- Assign and remove Mechanics from Service Tickets
- Postman collection included for testing

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Bernard445/Building-API-with-Application-Factory-Pattern.git
cd Building-API-with-Application-Factory-Pattern
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python
Database setup:

Create a MySQL database named mechanic_shop

Update database credentials in app/__init__.py if needed

Run the application:

bash
Copy code
python app.py
The API will be available at:

cpp
Copy code
http://127.0.0.1:5000
API Testing
A Postman collection JSON file is included in the repository

Import the collection into Postman to test all endpoints
