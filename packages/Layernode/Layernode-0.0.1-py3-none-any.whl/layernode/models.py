import time
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import uuid
from layernode import tools, custom


config, working_dir = custom.extract_configuration(dir=None, config=None)
db_setting = config['database']
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:3306/%s" % (
    db_setting['DB_USERNAME'], db_setting['DB_PASSWORD'], db_setting['DB_HOST'], db_setting['DATABASE_NAME'])

Base = declarative_base()


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    count = Column(Integer)

    def __init__(self, count):
        self.count = count

    def __repr__(self):
        return '<Count %r>' % self.count


class Provider(Base):
    __tablename__ = 'provider'
    address = Column(String(80), primary_key=True)
    name = Column(String(80), nullable=False)
    category = Column(String(80), nullable=False)
    balance = Column(Integer, default=0)
    approved = Column(Boolean, default=True)

    def __init__(self, address, name, category, approved, balance):
        self.address = address
        self.name = name
        self.category = category
        self.approved = approved
        self.balance = balance

    def __repr__(self):
        return '<Provider address: %s, name: %s, category: %s, approved: %s, balance: %s>' % (self.address, self.name, self.category, self.approved, self.balance)


class Layernode(Base):
    __tablename__ = 'layernode'
    address = Column(String(80), primary_key=True)
    url = Column(String(255), nullable=False)
    approved = Column(Boolean, default=True)

    def __init__(self, address, url, approved):
        self.address = address
        self.url = url
        self.approved = approved

    def __repr__(self):
        return '<Layernode address: %s, url: %s, approved: %s>' % (self.address, self.url, self.approved)


class Identity(Base):
    __tablename__ = 'identity'
    hash = Column(String(255), primary_key=True)  # identity_hash
    address = Column(String(255), nullable=False)  # provider address
    keyHash = Column(String(255), nullable=False)  # signer keyHash
    provider_sig = Column(String(255), nullable=False)
    signer_sig = Column(String(255), nullable=False)
    user_address = Column(String(80), ForeignKey('user.address'))
    user = relationship("User", backref="identities")

    def __init__(self, hash, address, keyHash, provider_sig, signer_sig, user):
        self.hash = hash
        self.address = address
        self.keyHash = keyHash
        self.provider_sig = provider_sig
        self.signer_sig = signer_sig
        self.user = user

    def __repr__(self):
        return '<Identity hash: %s, address: %s, keyHash: %s, provider_sig: %s, signer_sig: %s>' % (self.hash, self.address, self.keyHash, self.provider_sig, self.signer_sig)


class Score(Base):
    __tablename__ = 'score'
    id = Column(String(255), primary_key=True, default=str(uuid.uuid4()))
    address = Column(String(255), nullable=False)  # provider address
    hash = Column(String(255), nullable=False)
    keyHash = Column(String(255), nullable=False)
    score = Column(Integer, default=0)
    category = Column(String(255), nullable=False)
    provider_sig = Column(String(255), nullable=False)
    signer_sig = Column(String(255), nullable=False)

    def __init__(self, id, address, hash, keyHash, score, category, provider_sig, signer_sig):
        if not id:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.address = address
        self.hash = hash
        self.keyHash = keyHash
        self.score = score
        self.category = category
        self.provider_sig = provider_sig
        self.signer_sig = signer_sig

    def __repr__(self):
        return '<Score id: %s, address: %s, hash: %s, keyHash: %s, score: %s, category: %s, provider_sig: %s, signer_sig: %s>' % (self.id, self.address, self.hash, self.keyHash, self.score, self.category, self.provider_sig, self.signer_sig)


class Requests(Base):
    __tablename__ = 'requests'
    id = Column(String(255), primary_key=True, default=str(uuid.uuid4()))
    address = Column(String(255), nullable=False)  # provider address
    hash = Column(String(255), nullable=False)
    timestamp = Column(Integer, default=int(time.time()))
    provider_sig = Column(String(255), nullable=False)

    def __init__(self, id, address, hash, timestamp, provider_sig):
        if not id:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.address = address
        self.hash = hash
        self.timestamp = timestamp
        self.provider_sig = provider_sig

    def __repr__(self):
        return '<Requests id: %s, address: %s, hash: %s, timestamp: %s, provider_sig: %s>' % (self.id, self.address, self.hash, self.timestamp, self.provider_sig)


class User(Base):
    __tablename__ = 'user'
    address = Column(String(80), primary_key=True)

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return '<User address: %s>' % (self.address)


db_engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker()
session.configure(bind=db_engine)
Base.metadata.create_all(db_engine)
