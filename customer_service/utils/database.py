from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash
import time

db = SQLAlchemy()

start_time = None

def hash_password(password):
    """
    Hashes a plain-text password.
    :param password: Plain-text password
    :return: Hashed password
    """
    return generate_password_hash(password)

def init_db(app):
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
        # Import models to register them with SQLAlchemy
        from models.customer import Customer

        db.create_all()  # Create all tables
        with db.engine.connect() as connection:
            # Wrap the raw SQL query with `text`
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
