from flask import render_template

from blue.logic.logic import Logic
from blue.utilities.utilities import *
from flask_httpauth import HTTPBasicAuth

mod = Blueprint('site', __name__, template_folder='templates')

auth = HTTPBasicAuth()


@mod.route("/")
def index():
    logic = Logic()
    data = logic.get_current_week_sales()

    return render_template('index.html', count=logic.get_customers(), amount=logic.get_paymemts() )


@mod.route("/providers")
def provider():
    payments = MpesaPayment()
    return render_template('providers.html')
