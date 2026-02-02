# Mechanic Shop API

A RESTful API for managing a mechanic shop, built using Flask and the Application Factory pattern.  
This API supports customers, mechanics, vehicles, service tickets, and inventory with token-based authentication, pagination, and testing.

---

## 🚀 Features
- Customers, Mechanics, Vehicles, Service Tickets, Inventory
- JWT token authentication
- Pagination for customers
- Many-to-many relationships (mechanics ↔ service tickets)
- Rate limiting on login
- Caching on mechanics GET route
- Full unit test coverage using `unittest`
- Swagger API documentation

---

## 🛠️ Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- Marshmallow
- Flask-Limiter
- Flask-Caching
- Swagger (Flask-Swagger-UI)
- unittest

---

## 📦 Installation

Create virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
▶️ Run the App
python app.py
API will run at:

http://127.0.0.1:5000
Swagger Docs:

http://127.0.0.1:5000/apidocs
🧪 Run Tests
python -m unittest discover -s tests
🔐 Authentication
Login endpoint:

POST /customers/login
Returns:

{
  "status": "success",
  "auth_token": "TOKEN"
}
Use token in headers:

Authorization: Bearer TOKEN
📂 Project Structure
app/
  customers/
  mechanics/
  vehicles/
  service_tickets/
  inventory/
  utils/
tests/
swagger.yaml
app.py
📑 API Documentation
All routes are documented using Swagger:

/apidocs
Includes:

Endpoints

Request types

Parameters

Responses

Definitions
