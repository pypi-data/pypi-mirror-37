# HTTP Error Codes and their meaning: https://www.symantec.com/connect/articles/http-error-codes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dukepy.config import Config
from dukepy.sql_alchemy.tables.alchemy_base import AlchemyBase, db_uri, db_session

config = Config()

""" App """
## Init app
app = Flask(__name__)

## Init SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
if config["debug"]:
    app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app, model_class=AlchemyBase)
# db.create_all() # No use until the model classes are imported. Use scripts.create_db_schema instead.

""" Views """
# from app.views import

...
