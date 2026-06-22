from flask import Blueprint, render_template

generator_bp = Blueprint("generator", __name__)


@generator_bp.route("/generator")
def index():
    """
    Renders the password/passphrase generator UI.
    """
    return render_template("generator.html")
