#!/usr/bin/env python3


import os
from sqlalchemy import create_engine, Column, BigInteger, String, Text, Date, Table, ForeignKey, Boolean
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

users_topic = Table('users_topic', Model.metadata,
                    Column('users_id', ForeignKey('users.id')),
                    Column('topic_id', ForeignKey('topic.id'))
                    )


class Users(Model):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger)
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
    id = Column(BigInteger, primary_key=True)
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


class Message(Model):
    __tablename__ = 'message'
    id = Column(BigInteger, primary_key=True)
    message_telegram_id = Column(BigInteger)
    topic_id = Column(BigInteger, ForeignKey('topic.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    status = Column(String(50))
    type = Column(String(50))
    message_text = Column(Text)
    date = Column(Date)
    chat_id = Column(BigInteger)

    def __init__(self, id_, message_telegram_id, topic_id, user_id, status, type, message_text, date, chat_id):
        self.id = id_
        self.date = date
        self.topic_id = topic_id
        self.user_id = user_id
        self.status = status
        self.type = type
        self.message_text = message_text
        self.chat_id = chat_id
        self.message_telegram_id = message_telegram_id

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


class StateTopic(Model):
    __tablename__ = 'state_topic'
    id = Column(BigInteger, primary_key=True)
    topic_id = Column(BigInteger)
    telegram_id = Column(BigInteger)

    def __init__(self, id_, telegram_id, topic_id):
        self.id = id_
        self.telegram_id = telegram_id
        self.url = topic_id

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
