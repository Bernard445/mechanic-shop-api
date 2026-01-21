from flask import Blueprint, request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.extensions import db
from app.models import Customer
from app.customers.schemas import customer_schema, customers_schema

customers_bp = Blueprint('customers', __name__)

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


@customers_bp.route("/", methods=["GET"])
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers)


@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return {"message": "Customer not found"}, 404

    for key, value in request.json.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer)


@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return {"message": "Customer not found"}, 404

    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted"}
