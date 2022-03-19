#!/usr/bin/env python3


import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Table, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

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


class Users(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(200))
    admin = Column(Boolean)
    phone = Column(String(30))

    def __init__(self, user_id, telegram_id, first_name, last_name, username, admin, phone):
        self.id = user_id
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.admin = admin
        self.phone = phone

    def to_dict(self):
        res_prom = self.__dict__
        if res_prom.get("_sa_instance_state") is not None:
            res_prom.pop("_sa_instance_state")
        res = {}
        for key in res_prom:
            res[f'{self.__tablename__}_{key}'] = res_prom[key]
        return res

    def __str__(self):
        return self.__tablename__


class Topic(Model):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    url = Column(String(500))

    def __init__(self, theme_id, name, url):
        self.id = theme_id
        self.name = name
        self.url = url

    def to_dict(self):
        res_prom = self.__dict__
        if res_prom.get("_sa_instance_state") is not None:
            res_prom.pop("_sa_instance_state")
        res = {}
        for key in res_prom:
            res[f'{self.__tablename__}_{key}'] = res_prom[key]
        return res

    def __str__(self):
        return self.__tablename__


employ_theme = Table('users_topic', Model.metadata,
                     Column('users_id', ForeignKey('users.id')),
                     Column('topic_id', ForeignKey('topic.id'))
                     )


class Message(Model):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
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
        res_prom = self.__dict__
        if res_prom.get("_sa_instance_state") is not None:
            res_prom.pop("_sa_instance_state")
        res = {}
        for key in res_prom:
            res[f'{self.__tablename__}_{key}'] = res_prom[key]
        return res

    def __str__(self):
        return self.__tablename__


def init_migrate():
    Model.metadata.create_all(engine)
