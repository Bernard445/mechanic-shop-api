from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.extensions import db, limiter
from app.models import Customer
from app.customers import customers_bp
from app.customers.schemas import customer_schema, customers_schema, login_schema
from app.utils.util import encode_token, token_required


# ---------------- LOGIN ----------------
@customers_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    email = credentials["email"]
    password = credentials["password"]

    customer = db.session.execute(
        select(Customer).where(Customer.email == email)
    ).scalar_one_or_none()

    if not customer or customer.password != password:
        return jsonify({"message": "Invalid email or password"}), 401

    token = encode_token(customer.id)

    return jsonify({
        "status": "success",
        "auth_token": token
    }), 200


# ---------------- CREATE CUSTOMER ----------------
@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if customer.email:
        query = select(Customer).where(Customer.email == customer.email)
        if db.session.execute(query).scalars().first():
            return {"error": "Email already exists"}, 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


# ---------------- GET ALL CUSTOMERS ----------------
@customers_bp.route("/", methods=["GET"])
@token_required
def get_customers(customer_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)

    pagination = Customer.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "customers": customers_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200


# ---------------- GET ONE CUSTOMER ----------------
@customers_bp.route("/<int:id>", methods=["GET"])
@token_required
def get_customer_by_id(customer_id, id):
    customer = db.session.get(Customer, id)
    if not customer:
        return {"message": "Customer not found"}, 404
    return customer_schema.jsonify(customer), 200


# ---------------- UPDATE CUSTOMER ----------------
@customers_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(customer_id, id):
    customer = db.session.get(Customer, id)
    if not customer:
        return {"message": "Customer not found"}, 404

    for key, value in request.json.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# ---------------- DELETE CUSTOMER ----------------
@customers_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(customer_id, id):
    customer = db.session.get(Customer, id)
    if not customer:
        return {"message": "Customer not found"}, 404

    db.session.delete(customer)
    db.session.commit()
    return "", 204


# ---------------- MY TICKETS ----------------
@customers_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):

    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    tickets = []
    for vehicle in customer.vehicles:
        tickets.extend(vehicle.services)

    return jsonify([
        {
            "id": ticket.id,
            "description": ticket.description,
            "service_date": ticket.service_date.isoformat(),
            "cost": ticket.cost,
            "vehicle_id": ticket.vehicle_id
        }
        for ticket in tickets
    ]), 200
