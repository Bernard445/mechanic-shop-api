from flask import jsonify, request
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Inventory
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from app.utils.util import token_required


@service_tickets_bp.route("/", methods=["POST"])
@token_required
def create_service_ticket(customer_id):
    ticket = service_ticket_schema.load(request.json)
    db.session.add(ticket)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 201


@service_tickets_bp.route("/", methods=["GET"])
@token_required
def get_service_tickets(customer_id):
    tickets = db.session.query(ServiceTicket).all()
    return jsonify(service_tickets_schema.dump(tickets))


@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@token_required
def edit_ticket_mechanics(customer_id, ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found"}, 404

    data = request.json
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    # Add mechanics
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    # Remove mechanics
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.route("/<int:ticket_id>/add-part", methods=["POST"])
@token_required
def add_part_to_ticket(customer_id, ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return {"message": "Ticket not found"}, 404

    part_id = request.json.get("part_id")
    part = db.session.get(Inventory, part_id)
    if not part:
        return {"message": "Part not found"}, 404

    if part not in ticket.inventory:
        ticket.inventory.append(part)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))
