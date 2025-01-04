from flask import Flask, request, jsonify
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
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # Import models explicitly after initializing db
    from app.models.models import Customer, CustomerAccount, Product, Order, OrderProduct, User

    # Register models' metadata explicitly
    with app.app_context():
        db.create_all()  # Create all tables in the database
        app.logger.debug("App context is active.")
        app.logger.debug(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        app.logger.debug(f"Registered tables in metadata: {db.metadata.tables.keys()}")

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.customers import customers_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')

    # Error handling
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    return app
