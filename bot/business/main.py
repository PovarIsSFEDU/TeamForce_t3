from sqlalchemy import select, and_, func
from . import db_session


def insert(model, **kwargs):
    obj = model(**kwargs)
    db_session.add(obj)
    db_session.commit()


def update(model, id_, **kwargs):
    db_session.query(model).filter(model.id == id_).update(**kwargs)
    db_session.commit()


def delete(model, id_):
    db_session.query(model).filter(model.id == id_).delete()
    db_session.commit()


def convert_to_list(func):
    def foo(*args, **kwargs):
        res = func(*args, **kwargs)
        return [el[0].to_dict() for el in res]
    return foo


def select_max_id(model):
    stmt = select(func.max(model.id))
    res = db_session.execute(stmt).first()
    return res[0]


@convert_to_list
def select_all(model, operator=None):
    stmt = select(model)
    if operator is not None:
        stmt = stmt.where(operator)
        if isinstance(operator, list):
            stmt = stmt.where(and_(*operator))
    res = db_session.execute(stmt).all()
    return res




