from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SO%4012345@172.17.0.2:1433/application?driver=ODBC+Driver+17+for+SQL+Server'
    except:
        pass
    print("connected")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models.sales import Sales

        db.create_all()  # Create all tables
