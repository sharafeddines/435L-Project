from flask import Flask
from controllers.inventory_controller import inventory_bp, limiter

from utils.database import db, init_db
def create_app():
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    return app

if __name__ == '__main__':
    app = create_app()
    limiter.init_app(app)
    app.run(debug=True, host ="0.0.0.0")
