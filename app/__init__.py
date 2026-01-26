from flask import Flask
from app.extensions import db, ma, cache
from app.customers import customers_bp
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp
from app.vehicles import vehicles_bp
from app.extensions import limiter
from app.inventory import inventory_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+mysqlconnector://root:root@127.0.0.1:3307/mechanic_shop"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(vehicles_bp, url_prefix="/vehicles")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")


    print("\nREGISTERED ROUTES:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app
