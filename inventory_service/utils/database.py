from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import time

db = SQLAlchemy()

start_time = None

def init_db(app):
    """
    Initialize the database connection and create tables.

    This function configures the SQLAlchemy database URI, initializes the app context 
    for SQLAlchemy, and creates all required tables in the database.

    Args:
        app (Flask): The Flask application instance.

    Note:
        The database is assumed to be a Microsoft SQL Server instance configured via SQLAlchemy.
    """
    global start_time
    start_time = time.time()
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SO%4012345@192.168.1.2:1433/application?driver=ODBC+Driver+17+for+SQL+Server'
    except Exception:
        pass
    print("connected")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models.inventory import Inventory

        db.create_all()  # Create all tables

def check_db_connection():
    """
    Check the database connection and uptime.

    This function attempts to execute a simple query on the database to verify the connection. 
    It also calculates the elapsed time since the application started.

    Returns:
        tuple: A tuple containing:
            - bool: True if the database connection is successful, False otherwise.
            - float or None: The elapsed time since the application started (in seconds), or None if the connection failed.
    """
    try:
        elapsed_time = time.time() - start_time
        # Create a connection from the engine
        with db.engine.connect() as connection:
            # Wrap the raw SQL query with `text`
            result = connection.execute(text("SELECT 1"))
            print(f"Database query result: {result.fetchone()}")
        return True, elapsed_time
    except Exception as e:
        print(f"Database connection error: {e}")
        return False, None
