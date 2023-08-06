import click
import os
import db
import parse_xccd_ds
import load
import models
import ConfigParser
import api as scapinspector_api

from api import api
from api_static import api as api_static
from flask import Flask

config_file = os.path.expanduser('~/.scapinspector.cfg')
    
@click.group(chain=False)
def main():
    """
    Parse SCAP datastreams, result content and tailor custom profiles
    """
    pass

@main.command("init-db")
@click.option("--host")#, env_var="SCAPINSPECTOR_HOST")
@click.option("--user")#, env_var="SCAPINSPECTOR_USER")
@click.password_option() #, env_var="SCAPINSPECTOR_PASSWORD")
@click.option("--database") #, env_var="SCAPINSPECTOR_DB")
@click.option("--port") #, env_var="SCAPINSPECTOR_DB")
def init(host,user,password,database,port):
    """
    Initialize the Mysql storage db for data
    """
    db.set_mysql_config(host,user,password,database,port)
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.add_section('mariadb')
    config.set('mariadb', 'host'    , host)
    config.set('mariadb', 'user'    , user)
    config.set('mariadb', 'password', password)
    config.set('mariadb', 'database', database)
    config.set('mariadb', 'port'    , port)
    with open(config_file, 'wb') as configfile:
        config.write(configfile)
    models.build(True)
    pass

@main.command("show-config")
def show_config():
    """
    Show the configured db values
    """
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(config_file)
    host     = "localhost"
    user     = "root"
    password = ""
    database = ""
    port     = "3306"
    try:
        host     = config.get('mariadb', 'host')
        user     = config.get('mariadb', 'user')
        database = config.get('mariadb', 'database')
        password = config.get('mariadb', 'password')
        port     = config.get('mariadb', 'port')
    except Exception as ex:
        print("Configuration Error", ex)
    print("""
    Mariadb settings
      Host:     {0}
      Port:     {4}
      User:     {1}
      Password: {2}
      Database: {3}
    """.format(host,user,password,database,port))

    pass


def load_config():
    """
    Show the configured db values
    """
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(config_file)
    try:
        host     = config.get('mariadb', 'host')
        user     = config.get('mariadb', 'user')
        database = config.get('mariadb', 'database')
        password = config.get('mariadb', 'password')
        port     = config.get('mariadb', 'port')
        db.set_mysql_config(host,user,password,database,port)
    except Exception as ex:
        print("Configuration Error", ex)



@main.command("load-db")
def load_data():
    """
    Load a directory of scap datastreams into a custom database
    """
    directory="/usr/share/xml/scap/ssg/content/"
    load_config()
    session=db.get_db()
    if None == session: 
        print ("Init DB failed")
        exit(1)

    for dirname,dirnames, filenames in os.walk(directory):
        print("Dir:",dirname)
        for filename in filenames:
            print("File:",filename)
            if filename.endswith("-ds.xml"): 
                data=parse_xccd_ds.parse_datastream(directory+filename)
                #print (data)
                load.into_database(data)
                continue
            else:
                continue    
    pass


@main.command("get-benchmarks")
def benchmarks():
    """
    get benchmarks
    """
    load_config()
    results=scapinspector_api.get_benchmarks()
    print(results)

@main.command("ui")
def webserver():
    """
    run webserver
    """
    load_config()

    app = Flask(__name__, static_url_path='')
    app.register_blueprint(api)
    app.register_blueprint(api_static)
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()