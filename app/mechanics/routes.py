from flask import jsonify, request
from sqlalchemy import select
from app.extensions import db, cache
from app.models import Mechanic
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema
from app.utils.util import token_required


@mechanics_bp.route("/", methods=["POST"])
@token_required
def create_mechanic(customer_id):
    data = request.json

    if data.get("email"):
        existing = db.session.execute(
            select(Mechanic).where(Mechanic.email == data.get("email"))
        ).scalar_one_or_none()
        if existing:
            return jsonify({"error": "Email already exists"}), 400

    mechanic = mechanic_schema.load(data, session=db.session)
    db.session.add(mechanic)
    db.session.commit()

    return jsonify(mechanic_schema.dump(mechanic)), 201


@mechanics_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics)), 200


@mechanics_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_mechanic(customer_id, id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404

    for key, value in request.json.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200


@mechanics_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(customer_id, id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return {"message": "Mechanic not found"}, 404

    db.session.delete(mechanic)
    db.session.commit()
    return "", 204


@mechanics_bp.route("/most-worked", methods=["GET"])
def mechanics_most_worked():
    mechanics = Mechanic.query.all()
    sorted_mechanics = sorted(mechanics, key=lambda m: len(m.services), reverse=True)

    return jsonify([
        {"id": m.id, "name": m.name, "ticket_count": len(m.services)}
        for m in sorted_mechanics
    ]), 200
