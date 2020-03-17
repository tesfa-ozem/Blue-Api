from flask import request, jsonify, send_from_directory, json, render_template
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from blue.utilities.utilities import *
from blue import create_app
import os
from flask_httpauth import HTTPBasicAuth

mod = Blueprint('site', __name__)

auth = HTTPBasicAuth()


@mod.route("/")
def index():
    render_template()
