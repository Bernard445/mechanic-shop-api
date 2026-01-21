from flask import request, jsonify
from app.extensions import db
from app.models import Vehicle
from app.vehicles import vehicles_bp
from app.vehicles.schemas import vehicle_schema, vehicles_schema

@vehicles_bp.route("/", methods=["POST"])
def create_vehicle():
    vehicle = vehicle_schema.load(request.json, session=db.session)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle_schema.dump(vehicle)), 201


@vehicles_bp.route("/", methods=["GET"])
def get_vehicles():
    vehicles = db.session.query(Vehicle).all()
    return jsonify(vehicles_schema.dump(vehicles))
