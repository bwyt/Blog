from flask import Blueprint

main_blu = Blueprint('main', __name__)

from app.main import routes