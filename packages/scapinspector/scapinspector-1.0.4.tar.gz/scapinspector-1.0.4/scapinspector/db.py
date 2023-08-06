global mysql_config
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

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db_conn=None
mysql_config=None

def set_mysql_config(host,user,password,database,port):
    global mysql_config
    mysql_config={}
    mysql_config['user']    = user
    mysql_config['password']= password
    mysql_config['host']    = host
    mysql_config['database']= database
    mysql_config['port']    = port



def get_mysql_config():
    global mysql_config
    config={}
    if mysql_config==None:
        mysql_config={}

    if 'user' not in  mysql_config:
        config['user']     = os.environ.get('SCAPINSPECTOR_DB_USER') 
    else:
        config['user']=mysql_config['user']

    if 'password' not in mysql_config:
        config['password'] = os.environ.get('SCAPINSPECTORT_DB_PASS')
    else:
        config['password']=mysql_config['password']

    if 'host' not in mysql_config:
        config['host']     = os.environ.get('SCAPINSPECTOR_DB_HOST') 
    else:
        config['host']=mysql_config['host']

    if 'database' not in mysql_config:
        config['database'] = os.environ.get('SCAPINSPECTOR_DB_NAME') 
    else:
        config['database']=mysql_config['database']

    if 'port' not in  mysql_config:
        config['port']     = os.environ.get('SCAPINSPECTOR_PORT') 
    else:
        config['port']=mysql_config['port']
    
    if None == config['port']:
        config['port']='3306'
    return config



def connect():

    mysql_config=get_mysql_config()

    if  None == mysql_config :
        connect_string = "mysql+pymysql://{}@{}:{}/{}?charset=utf8mb4".format( mysql_config['user'],
                                                                            mysql_config['host'],
                                                                            mysql_config['port'],
                                                                            mysql_config['database']
                                                                            )
    else:    
        connect_string = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format( mysql_config['user'],
                                                                            mysql_config['password'],
                                                                            mysql_config['host'],
                                                                            mysql_config['port'],
                                                                            mysql_config['database']
                                                                            )


    #print (connect_string)
    engine = create_engine(connect_string, convert_unicode=True, echo=False)
    Session = sessionmaker(bind=engine)
    session=Session()
    return {'session':session,'engine':engine}



def get_db():
    global db_conn
    try:
        if 'db' not in g:
            g.db = connect()
        return g.db
    except :
        db_conn=connect()
        return db_conn





def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

