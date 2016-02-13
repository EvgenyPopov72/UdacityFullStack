from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

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

    def __repr__(self):
        return '<Puppy %s' % self.name


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def __repr__(self):
        return '<Owner %s' % self.name


entities = {
    'puppy': Puppy,
    'shelter': Shelter,
    'owner': Owner
}

# engine = create_engine('sqlite:///puppyshelter.db')
engine = create_engine('postgresql://postgres:postgres@localhost/puppies')
Base.metadata.create_all(engine)
