#!/usr/bin/env python3


import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.environ.get("POSTGRES_USER")
psw = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT")
db = os.environ.get("POSTGRES_DB")

engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(user, psw, host, port, db))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Model = declarative_base(name='Model')


class Employ(Model):
    __tablename__ = 'employ'
    id = Column('employ_id', Integer, primary_key=True)
    name = Column(String(200))
    project_name = Column(String(200))
    message = Column(Text)
    date_message = Column(Date)

    def __init__(self, employ_id,  name, project_name, date_message):
        self.id = employ_id
        self.name = name
        self.project_name = project_name
        self.date_message = date_message


def init_migrate():
    Model.metadata.create_all(engine)


