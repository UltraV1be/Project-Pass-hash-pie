from flask import Blueprint, render_template

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analysis")
def index():
    """
    Renders the password analysis dashboard UI.
    """
    return render_template("analysis.html")
