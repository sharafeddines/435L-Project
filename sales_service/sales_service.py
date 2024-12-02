from flask import Flask
from controllers.sales_controller import sales_bp, limiter
from sales_profiler import profile_functions

from utils.database import db, init_db
def create_app():
    """
    Create and configure the Flask application.

    This function initializes the database, sets up necessary configurations, 
    and registers the blueprints for handling routes.

    :return: The configured Flask application instance.
    :rtype: flask.Flask
    """
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(sales_bp, url_prefix="/sales")
    return app

if __name__ == '__main__':
    """
    Entry point for running the Flask application.

    This block initializes the Flask app, sets up rate-limiting, 
    and starts the development server on host `0.0.0.0` with debug mode enabled.
    """
    app = create_app()
    limiter.init_app(app)
    profile_functions(app)
    app.run(debug=True, host ="0.0.0.0")
