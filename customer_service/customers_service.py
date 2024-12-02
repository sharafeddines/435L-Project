from flask import Flask
from controllers.customer_controller import customer_bp, limiter
from services.customer_service import register_customer
from customer_profiler import profile_functions
from utils.database import db, init_db

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, sets up the database,
    and registers the necessary blueprints.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    print("attempting connection")
    
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(customer_bp, url_prefix="/customers")
    return app

if __name__ == '__main__':
    """
    Entry point for running the Flask application.

    This block creates the Flask application using `create_app`, initializes
    the rate limiter, and starts the development server on `0.0.0.0` with
    debugging enabled.
    """
    app = create_app()
    limiter.init_app(app)
    profile_functions(app)
    app.run(debug=True, host="0.0.0.0")
    
