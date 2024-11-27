from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SO%4012345@172.17.0.2:1433/application?driver=ODBC+Driver+17+for+SQL+Server&timeout=30'
    except:
        pass
    print("connected")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models.customer import Customer

        db.create_all()  # Create all tables
