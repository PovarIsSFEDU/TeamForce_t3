#!/usr/bin/env python3


import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Table, ForeignKey, Boolean
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
    id = Column(Integer, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(200))
    admin = Column(Boolean)
    phone = Column(String(30))

    def __init__(self, employ_id, first_name, last_name, username, admin, phone):
        self.id = employ_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.admin = admin
        self.phone = phone

    def to_dict(self):
        res = self.__dict__
        if res.get("_sa_instance_state") is not None:
            res.pop("_sa_instance_state")
        return res


class Theme(Model):
    __tablename__ = 'theme'
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    url = Column(String(500))

    def __init__(self, theme_id, name, url):
        self.id = theme_id
        self.name = name
        self.url = url

    def to_dict(self):
        res = self.__dict__
        if res.get("_sa_instance_state") is not None:
            res.pop("_sa_instance_state")
        return res

employ_theme = Table('employ_theme', Model.metadata,
                     Column('employ_id', ForeignKey('employ.id')),
                     Column('theme_id', ForeignKey('theme.id'))
                     )


class Message(Model):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, ForeignKey('theme.id'))
    employ_id = Column(Integer, ForeignKey('employ.id'))
    status = Column(String(50))
    type = Column(String(50))
    message_text = Column(Text)
    date = Column(Date)

    def __init__(self, employ_id, name, project_name, date_message):
        self.id = employ_id
        self.name = name
        self.project_name = project_name
        self.date_message = date_message

    def to_dict(self):
        res = self.__dict__
        if res.get("_sa_instance_state") is not None:
            res.pop("_sa_instance_state")
        return res


def init_migrate():
    Model.metadata.create_all(engine)
