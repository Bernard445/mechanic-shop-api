from marshmallow_sqlalchemy import auto_field
from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    email = auto_field()
    phone = auto_field()
    address = auto_field()

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)