import os

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# from puppies import app

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('puppy_id', Integer, ForeignKey('puppy.id')),
                          Column('owner_id', Integer, ForeignKey('owner.id'))
                          )


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)

    def __repr__(self):
        return '<Shelter %s' % self.name


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    weight = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

    owner = relationship('Owner', secondary='association', backref='puppy')

    def __repr__(self):
        return '<Puppy %s' % self.name


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250))
    puppy = relationship('Puppy', secondary='association', backref='owner')

    def __repr__(self):
        return '<Owner %s' % self.name


entities = {
    'puppy': Puppy,
    'shelter': Shelter,
    'owner': Owner
}

database_uri = os.environ.get('DATABASE_URL')
# database_uri = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(database_uri)
# Base.metadata.create_all(engine)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
