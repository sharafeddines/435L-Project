from flask import Flask
from controllers.review_controller import review_bp, limiter

from utils.database import db, init_db
def create_app():
    """
    Create and configure the Flask application.

    :return: The Flask application instance.
    :rtype: flask.Flask
    """
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(review_bp, url_prefix="/review")
    return app

if __name__ == '__main__':
    """
    The entry point of the application. Initializes the Flask app and runs the development server.

    Initializes rate-limiting and runs the Flask app on host 0.0.0.0 with debug mode enabled.
    """
    app = create_app()
    limiter.init_app(app)
    app.run(debug=True, host ="0.0.0.0")
