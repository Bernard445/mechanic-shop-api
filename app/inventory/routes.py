from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from app.inventory import inventory_bp
from app.inventory.schemas import inventory_schema, inventories_schema
from app.utils.util import token_required


@inventory_bp.route("/", methods=["POST"])
@token_required
def create_part(customer_id):
    data = request.get_json()
    new_part = Inventory(**data)
    db.session.add(new_part)
    db.session.commit()
    return jsonify(inventory_schema.dump(new_part)), 201


@inventory_bp.route("/", methods=["GET"])
@token_required
def get_inventory(customer_id):
    parts = db.session.query(Inventory).all()
    return jsonify(inventories_schema.dump(parts)), 200


@inventory_bp.route("/<int:part_id>", methods=["PUT"])
@token_required
def update_part(customer_id, part_id):
    part = db.session.query(Inventory).filter_by(id=part_id).first()
    if not part:
        return jsonify({"error": "Part not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return jsonify(inventory_schema.dump(part)), 200


@inventory_bp.route("/<int:part_id>", methods=["DELETE"])
@token_required
def delete_part(customer_id, part_id):
    part = db.session.query(Inventory).filter_by(id=part_id).first()
    if not part:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted"}), 200