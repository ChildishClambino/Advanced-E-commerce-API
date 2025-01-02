from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.config import Config
import logging

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # Log incoming requests
    @app.before_request
    def log_request():
        app.logger.info(f"Handling request: {request.method} {request.path}")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    jwt = JWTManager(app)

    # Log app context explicitly
    with app.app_context():
        app.logger.debug("App context is active.")
        app.logger.debug(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

        # Import models explicitly to register them
        from app.models.models import Customer, CustomerAccount, Product, Order, OrderProduct, User

        # Log metadata before applying migrations
        app.logger.debug(f"Metadata tables: {db.metadata.tables.keys()}")

        # Ensure all tables are registered
        if 'users' not in db.metadata.tables:
            app.logger.error("Users table is missing in metadata.")

    # Register blueprints
    from app.routes.customers import customers_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(customers_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app
