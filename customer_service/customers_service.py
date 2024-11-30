from flask import Flask
from controllers.customer_controller import customer_bp, limiter
from services.customer_service import register_customer

from utils.database import db, init_db


def create_app():
    app = Flask(__name__)
    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(customer_bp, url_prefix="/customers")
    return app

if __name__ == '__main__':
    app = create_app()
    limiter.init_app(app)
    app.run(debug=True, host ="0.0.0.0")
    
