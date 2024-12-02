from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import time

db = SQLAlchemy()

start_time = None

def init_db(app):
    """
    Initialize the database with the Flask application.

    This function sets up the SQLAlchemy database connection, configures the database URI,
    and creates the necessary tables based on the registered models.

    :param app: The Flask application instance.
    :type app: flask.Flask
    :raises Exception: If there is an error in setting the database URI.
    """
    global start_time 
    start_time = time.time()
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SO%4012345@127.0.0.1:1433/application?driver=ODBC+Driver+17+for+SQL+Server'
    except:
        pass
    print("connected")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models.sales import Sales

        db.create_all()  # Create all tables

def check_db_connection():
    """
    Check the database connection and measure the service uptime.

    This function attempts to establish a connection with the database and runs a basic query to verify connectivity.
    It also calculates the elapsed time since the database initialization.

    :return: A tuple containing:
        - A boolean indicating the connection status (True if successful, False otherwise).
        - The elapsed time since the database was initialized (in seconds), or None if the connection fails.
    :rtype: tuple(bool, float or None)
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