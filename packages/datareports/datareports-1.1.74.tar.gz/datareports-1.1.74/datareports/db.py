import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import click
from flask import current_app, g
from flask.cli import with_appcontext

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db_conn=None

def connect():
    mysql_config = {
        'user'     : os.environ.get('DATAREPORTS_DB_USER') ,
        'password' : os.environ.get('DATAREPORTS_DB_PASS') ,
        'host'     : os.environ.get('DATAREPORTS_DB_HOST') ,
        'database' : os.environ.get('DATAREPORTS_DB_NAME') 
    }

    connect_string = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format( mysql_config['user'],
                                                                           mysql_config['password'],
                                                                           mysql_config['host'],
                                                                           mysql_config['database'])

    #print (mysql_config)
    engine = create_engine(connect_string, convert_unicode=True, echo=False)
    Session = sessionmaker(bind=engine)
    session=Session()
    return {'session':session,'engine':engine}


def get_db(app):
    global db_conn
    # if no flask
    if None == g:
        if None == db_conn:
            db_conn=connect()
        return db_conn
    #if flask
    if 'db' not in g:
        g.db =connect()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

