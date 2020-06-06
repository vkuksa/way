from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
def front():
    return render_template('home.html', title='Home')

