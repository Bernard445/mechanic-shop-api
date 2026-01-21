from flask import Blueprint

mechanics_bp = Blueprint("mechanics", __name__)

from app.mechanics.routes import *  # <-- THIS LINE IS REQUIRED
