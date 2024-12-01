from flask import Flask
from controllers.inventory_controller import inventory_bp, limiter
from utils.database import db, init_db

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, sets up the database connection,
    and registers the necessary blueprints, including the inventory controller.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    return app

if __name__ == '__main__':
    """
    Entry point for running the Flask application.

    This block creates the Flask application using `create_app`, initializes
    the rate limiter, and starts the development server on `0.0.0.0` with debugging enabled.
    """
    app = create_app()
    limiter.init_app(app)
    app.run(debug=True, host="0.0.0.0")
