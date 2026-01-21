from flask import request
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from flask import jsonify

@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    ticket = service_ticket_schema.load(request.json)
    db.session.add(ticket)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 201


@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return jsonify(service_tickets_schema.dump(tickets))


@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return {"message": "Ticket or Mechanic not found"}, 404

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mechanic:
        return {"message": "Ticket or Mechanic not found"}, 404

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))