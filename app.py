from flask import Flask
from controllers.customer_controller import customer_bp
from controllers.inventory_controller import inventory_bp
from utils.database import db, init_db
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///customers.db'  # Database URI


    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
