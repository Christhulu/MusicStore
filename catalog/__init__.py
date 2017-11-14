"""
    Catalog App Initialization.
    Initialize the Flask framework.
    Initialize the SQLAlchemy ORM.
"""


from flask import Flask


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Initialize Flask framework
app = Flask(__name__)
app.config.from_object('config')



# Connect to database
engine = create_engine(app.config['DATABASE_URI'])

# Get a database session object
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Flask view functions
import catalog.views





