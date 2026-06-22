from flask import Blueprint, render_template

hashing_bp = Blueprint("hashing", __name__)


@hashing_bp.route("/hashing")
def index():
    """
    Renders the hashing workbench laboratory UI.
    """
    return render_template("hashing.html")
