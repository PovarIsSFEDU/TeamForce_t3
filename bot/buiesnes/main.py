from sqlalchemy import select
from . import db_session


def insert(model, **kwargs):
    obj = model(**kwargs)
    db_session.add(obj)
    db_session.commit()


def convert_to_list(func):
    def foo(*args, **kwargs):
        res = func(*args, **kwargs)
        return [el[0].to_dict() for el in res]
    return foo


@convert_to_list
def select_all(model):
    stmt = select(model)
    res = db_session.execute(stmt).all()
    return res




