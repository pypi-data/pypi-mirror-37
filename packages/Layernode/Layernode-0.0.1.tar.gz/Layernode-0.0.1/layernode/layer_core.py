from layernode import tools
from layernode.models import *
from sqlalchemy import func
import pprint


def row2dict(r): return {c.name: getattr(r, c.name)
                         for c in r.__table__.columns}


def calc_score(address, hash):
    # address: provider address
    # hash: identity_hash
    db_session = session()
    score_rows = db_session.query(Score).filter(
        Score.address == address, Score.hash == hash).all()
    
    if len(score_rows) > 0:
        prs = 0
        lrs = 0
        for row in score_rows:
            prs = prs + row.score
            lrs = lrs + row.score

        prs = prs / len(score_rows)
        lrs = lrs / len(score_rows)
        return {"prs": prs, "lrs": lrs}
    else:
        return None


def get_score_length():
    db_session = session()
    length = db_session.query(func.count(Score.id)).scalar() - 1
    return length


def get_score(length):
    db_session = session()
    row = db_session.query(Score).offset(length).first()
    result = None
    try:
        result = row2dict(row)
        result['length'] = length
    except Exception as e:
        print('row2dict get_score error', e)
        print('row = ', row)
    return result


def get_identity_length():
    db_session = session()
    length = db_session.query(func.count(Identity.hash)).scalar() - 1
    return length


def get_identity(identity_length):
    db_session = session()
    row = db_session.query(Identity).offset(identity_length).first()
    result = None
    try:
        result = row2dict(row)
        result['identity_length'] = identity_length
    except Exception as e:
        pass
    return result


def get_request_count_by_provider(address):
    db_session = session()
    length = db_session.query(Requests).filter_by(address=address).count()
    return length


def get_request_length():
    db_session = session()
    length = db_session.query(func.count(Requests.hash)).scalar() - 1
    return length


def get_request(request_length):
    db_session = session()
    row = db_session.query(Requests).offset(request_length).first()
    result = None
    try:
        result = row2dict(row)
        result['request_length'] = request_length
    except Exception as e:
        pass
    return result
