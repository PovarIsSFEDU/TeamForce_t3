from sqlalchemy import select, and_, func
from . import db_session, Users, Topic, Message
import sqlalchemy


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


def checked(el):
    return isinstance(el, Users) or isinstance(el, Topic) or isinstance(el, Message)


def convert_to_list(func):
    def foo(*args, **kwargs):
        res = func(*args, **kwargs)
        result = []
        if res:
            if isinstance(res, list):
                if isinstance(res[0], dict):
                    return res
                if isinstance(res[0], sqlalchemy.engine.row.Row):
                    for shingle in res:
                        dict_prom = {}
                        for el in shingle:
                            if isinstance(el, str) or isinstance(el, int):
                                result.append(el)
                            else:
                                dict_prom.update(el.to_dict())
                        if dict_prom:
                            result.append(dict_prom)
                    return result
        return res
    return foo


def select_max_id(model):
    stmt = select(func.max(model.id))
    res = db_session.execute(stmt).first()
    return res[0]


@convert_to_list
def get_theme_by_user(id_):
    res = db_session.query(Users, Topic).filter(Users.id == id_).all()
    return res


@convert_to_list
def select_all(model, operator=None):
    stmt = select(model)
    if operator is not None:
        stmt = stmt.where(operator)
        if isinstance(operator, list):
            stmt = stmt.where(and_(*operator))
    res = db_session.execute(stmt).all()
    return res




