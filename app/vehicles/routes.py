from flask import request, jsonify
from app.extensions import db
from app.models import Vehicle
from app.vehicles import vehicles_bp
from app.vehicles.schemas import vehicle_schema, vehicles_schema
from app.utils.util import token_required


@vehicles_bp.route("/", methods=["GET"])
@token_required
def get_vehicles(customer_id):
    vehicles = Vehicle.query.all()
    return jsonify(vehicles_schema.dump(vehicles)), 200


@vehicles_bp.route("/", methods=["POST"])
@token_required
def create_vehicle(customer_id):
    vehicle = vehicle_schema.load(request.json, session=db.session)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle_schema.dump(vehicle)), 201


@vehicles_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_vehicle(customer_id, id):
    vehicle = db.session.get(Vehicle, id)
    if not vehicle:
        return {"message": "Vehicle not found"}, 404

    for key, value in request.json.items():
        setattr(vehicle, key, value)

    db.session.commit()
    return jsonify(vehicle_schema.dump(vehicle)), 200


@vehicles_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_vehicle(customer_id, id):
    vehicle = db.session.get(Vehicle, id)
    if not vehicle:
        return {"message": "Vehicle not found"}, 404

    db.session.delete(vehicle)
    db.session.commit()
    return "", 204
