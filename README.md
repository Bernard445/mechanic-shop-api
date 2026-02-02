🛠 Mechanic Shop API

A RESTful Flask API for managing a mechanic shop.
This project supports customers, vehicles, service tickets, mechanics, and inventory with authentication, rate limiting, caching, and relational data modeling.

🚀 Features

JWT Token Authentication (python-jose)

Rate Limiting (Flask-Limiter)

Caching (Flask-Caching)

Pagination

Many-to-Many Relationships

Secure protected routes

Inventory tracking system

Postman-tested endpoints

🧩 Technologies Used

Python

Flask

Flask-SQLAlchemy

Flask-Marshmallow

Flask-Limiter

Flask-Caching

MySQL

python-jose

Postman

🔐 Authentication

Users authenticate via:

POST /customers/login


Returns a JWT token.
Protected routes require a header:

Authorization: Bearer <token>

📦 API Resources
Customers

POST /customers – Create customer

POST /customers/login – Login and receive token

GET /customers – Get paginated customers

PUT /customers/<id> – Update customer (protected)

DELETE /customers/<id> – Delete customer (protected)

GET /customers/my-tickets – Get logged-in customer’s service tickets

Mechanics

POST /mechanics – Create mechanic (protected)

GET /mechanics – Get all mechanics (cached)

PUT /mechanics/<id> – Update mechanic (protected)

DELETE /mechanics/<id> – Delete mechanic (protected)

GET /mechanics/most-worked – Sorted by number of tickets worked

Vehicles

POST /vehicles – Create vehicle

GET /vehicles – Get all vehicles

Service Tickets

POST /service-tickets – Create ticket (protected)

GET /service-tickets – Get all tickets (protected)

PUT /service-tickets/<ticket_id>/edit – Add/remove mechanics

POST /service-tickets/<ticket_id>/add-part – Add inventory part to ticket

Inventory

POST /inventory – Create part (protected)

GET /inventory – Get all parts (protected)

PUT /inventory/<id> – Update part (protected)

DELETE /inventory/<id> – Delete part (protected)

🧠 Data Relationships

One Customer → Many Vehicles

One Vehicle → Many Service Tickets

Service Tickets ↔ Mechanics (Many-to-Many)

Service Tickets ↔ Inventory Parts (Many-to-Many)
