from marshmallow import fields
from marshmallow_sqlalchemy import auto_field
from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = auto_field(dump_only=True)
    first_name = auto_field(required=True)
    last_name = auto_field(required=True)
    email = auto_field(required=True)
    password = fields.String(load_only=True, required=True)  # ✅ FIXED
    phone = auto_field()
    address = auto_field()

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()