import os
from flask import Flask, render_template

# Import blueprints
from routes.api_routes import api_bp
from routes.analysis_routes import analysis_bp
from routes.generator_routes import generator_bp
from routes.breach_routes import breach_bp
from routes.hashing_routes import hashing_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(generator_bp)
    app.register_blueprint(breach_bp)
    app.register_blueprint(hashing_bp)

    # Main dashboard landing routes
    @app.route("/")
    def index():
        """
        Renders the application landing page.
        """
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        """
        Renders the security intelligence control center.
        """
        return render_template("dashboard.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("base.html", error="404 Page Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return (
            render_template("base.html", error="500 Internal Server Error"),
            500,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    # Bind to localhost standard port
    app.run(host="127.0.0.1", port=port, debug=app.config["DEBUG"])
