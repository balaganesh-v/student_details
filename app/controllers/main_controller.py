from flask import Blueprint,render_template

main_bp = Blueprint('main',__name__)


@main_bp.route("/")
def login():
    return render_template("login_page/landing_page.html")

@main_bp.route("/index_page")
def index_page():
    return render_template("index.html")