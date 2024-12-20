from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    account = db.relationship('CustomerAccount', back_populates='customer', uselist=False, cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='customer', cascade="all, delete-orphan")

# CustomerAccount Model
class CustomerAccount(db.Model):
    __tablename__ = 'customer_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='account')

# Product Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_items = db.relationship('OrderProduct', back_populates='product', cascade="all, delete-orphan")

# Order Model
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')
    products = db.relationship('OrderProduct', back_populates='order', cascade="all, delete-orphan")

# OrderProduct Model
class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='order_items')

# Debug print to check metadata
print("Metadata tables after model definitions:", db.metadata.tables.keys())
print("Final metadata tables in models:", db.metadata.tables.keys())
