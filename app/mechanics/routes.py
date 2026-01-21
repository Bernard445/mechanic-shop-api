from flask import request
from app import mechanics
from app.extensions import db
from app.models import Mechanic
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import jsonify, request
from sqlalchemy import select


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    data = request.json

    # Check for duplicate email
    existing = db.session.execute(
        select(Mechanic).where(Mechanic.email == data.get("email"))
    ).scalar_one_or_none()

    if existing:
        return jsonify({"error": "Email already exists"}), 400

    mechanic = mechanic_schema.load(data)
    db.session.add(mechanic)
    db.session.commit()

    return jsonify(mechanic_schema.dump(mechanic)), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return jsonify(mechanics_schema.dump(mechanics))

@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404

    for key, value in request.json.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic))

@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404

    db.session.delete(mechanic)
    db.session.commit()
    return {"message": "Mechanic deleted"}
