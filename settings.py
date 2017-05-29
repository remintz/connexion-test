# Flask settings
FLASK_SERVER_NAME = 'localhost:8080'
FLASK_SERVER_PORT = 8080
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI_UNITTEST = 'sqlite:///dbtest.sqlite'

# Set to true if you want to reset the database on next run
# REMEMBER TO SET BACK TO FALSE AGAIN!!!
RESET_DATABASE = True