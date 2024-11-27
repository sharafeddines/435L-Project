from flask import Flask
from controllers.sales_controller import sales_bp

from utils.database import db, init_db
def create_app():
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(sales_bp, url_prefix="/sales")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host ="0.0.0.0")