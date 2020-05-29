from flask import render_template, request, Blueprint
from way.models import Article

main = Blueprint('main', __name__)


@main.route("/")
def front():
    return render_template('home.html', title='Home')

