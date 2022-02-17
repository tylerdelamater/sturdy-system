# coding=utf-8
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib

if os.environ['ENV'] == 'dev':
    print('using dev db')
    db_url = 'localhost:5432'
    db_name = 'online-exam'
    db_user = 'postgres'
    db_password = '0NLIN3-ex4m'
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
else:
    #Driver={ODBC Driver 13 for SQL Server};Server=tcp:online-exam.database.windows.net,1433;Database=online-exam;Uid=onlineexamadmin;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
    server = 'online-exam.database.windows.net'
    database = 'online-exam'
    username = 'onlineexamadmin'
    password = "m'3`fs|9ciL?p|E"
    driver = '{ODBC Driver 13 for SQL Server}'
    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.quote_plus(odbc_str)
    engine = create_engine(connect_str)


Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_updated_by = Column(String)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by