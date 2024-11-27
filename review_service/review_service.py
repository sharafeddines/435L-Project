from flask import Flask
from controllers.review_controller import review_bp

from utils.database import db, init_db
def create_app():
    app = Flask(__name__)

    print("attempting connection")
    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(review_bp, url_prefix="/review")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host ="0.0.0.0")
