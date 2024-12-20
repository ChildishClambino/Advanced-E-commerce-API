from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import all models explicitly to ensure they are registered
        from app.models.models import Customer, CustomerAccount, Product, Order, OrderProduct

        # Debugging: Log metadata tables
        print("Metadata tables after model definitions:", db.metadata.tables.keys())

        # Drop and recreate tables
        try:
            print("Dropping all tables...")
            db.drop_all()
            print("Tables dropped successfully!")

            print("Creating all tables using db.create_all()...")
            db.create_all()
            print("Tables created successfully! Metadata tables after db.create_all:", db.metadata.tables.keys())
        except Exception as e:
            print(f"Error during table creation: {e}")

        # Test raw SQL execution for further debugging
        try:
            print("Testing raw SQL...")
            with db.engine.connect() as connection:
                connection.execute(db.text("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100)
                    );
                """))
                print("Raw SQL table created!")
                connection.execute(db.text("DROP TABLE IF EXISTS test_table;"))
                print("Raw SQL table dropped!")
        except Exception as e:
            print(f"Error during raw SQL execution: {e}")

    return app
