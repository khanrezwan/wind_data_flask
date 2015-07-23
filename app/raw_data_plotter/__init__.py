from flask import Blueprint
raw_data_plotter = Blueprint('raw_data_plotter', __name__)
from . import views, errors
