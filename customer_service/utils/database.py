from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash
import time

db = SQLAlchemy()

start_time = None

def hash_password(password):
    """
    Hashes a plain-text password.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return generate_password_hash(password)

def init_db(app):
    """
    Initialize the database connection and create tables.

    This function configures the SQLAlchemy database URI,
    initializes the app context for SQLAlchemy, and creates
    all required tables in the database. It also inserts a
    default admin user if it doesn't already exist.

    Args:
        app (Flask): The Flask application instance.

    Note:
        The database is assumed to be a Microsoft SQL Server
        instance configured via SQLAlchemy.
    """
    global start_time 
    start_time = time.time()
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:SO%4012345@192.168.1.2:1433/application?driver=ODBC+Driver+17+for+SQL+Server&timeout=30'
    except:
        pass
    print("connected")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        from models.customer import Customer

        db.create_all()  # Create all tables
        with db.engine.connect() as connection:
            try:
                password_admin = hash_password("admin")
                result = connection.execute(text("""
                INSERT INTO Customers (full_name, username, password_hash, age, address, gender, marital_status, is_admin)
                VALUES (:full_name, :username, :password_hash, :age, :address, :gender, :marital_status, :is_admin)
                """), {
                    "full_name": "admin",
                    "username": "admin",
                    "password_hash": password_admin,
                    "age": 0,
                    "address": "blank",
                    "gender": "M",
                    "marital_status": "na",
                    "is_admin": True
                })
                connection.commit()
            except:
                pass

def check_db_connection():
    """
    Check the database connection and uptime.

    This function attempts to execute a simple query on the
    database to verify the connection. It also calculates the
    elapsed time since the application started.

    Returns:
        tuple: A tuple containing:
            - bool: True if the database connection is successful, False otherwise.
            - float or None: The elapsed time since the application started
              (in seconds), or None if the connection failed.
    """
    try:
        elapsed_time = time.time() - start_time
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Database query result: {result.fetchone()}")
        return True, elapsed_time
    except Exception as e:
        print(f"Database connection error: {e}")
        return False, None
