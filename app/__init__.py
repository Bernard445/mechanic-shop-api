import os
from flask import Flask
from app.extensions import db, ma, cache, limiter
from app.customers import customers_bp
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp
from app.vehicles import vehicles_bp
from app.inventory import inventory_bp
from flasgger import Swagger


def create_app(config_name=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "mysql+mysqlconnector://root:root@127.0.0.1:3307/mechanic_shop"
)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()


    Swagger(app, template_file=os.path.join(os.path.dirname(__file__), "swagger.yaml"))

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(vehicles_bp, url_prefix="/vehicles")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app
