class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Like214!@localhost/ecommerce_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Enable SQL logging
    SECRET_KEY = 'your_secret_key'
