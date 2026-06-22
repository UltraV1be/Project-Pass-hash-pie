from flask import Blueprint, render_template

breach_bp = Blueprint("breach", __name__)


@breach_bp.route("/breach")
def index():
    """
    Renders the HaveIBeenPwned database breach check UI.
    """
    return render_template("breach.html")
