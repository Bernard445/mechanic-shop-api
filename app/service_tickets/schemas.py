from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import ServiceTicket
from app.extensions import db

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session
        include_fk = True


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

