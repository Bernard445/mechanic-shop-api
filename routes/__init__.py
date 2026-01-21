from flask import Flask
from app.extensions import db, ma
from app.routes.customers import customers_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+mysqlconnector://root:root@127.0.0.1:3307/mechanic_shop'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(customers_bp)

    with app.app_context():
        db.create_all()

    return app
