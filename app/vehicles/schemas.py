from app.extensions import ma
from app.models import Vehicle
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class VehicleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        include_fk = True

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
