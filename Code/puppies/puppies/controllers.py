from models import entities, session

# engine = create_engine('sqlite:///puppyshelter.db')
# engine = create_engine('postgresql://postgres:postgres@localhost/puppies')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


def getItemsList(items):
    return session.query(items).order_by(items.name).all()


def addUpdateItem(item):
    session.add(item)
    return session.commit()


def deleteExistingItem(item):
    session.delete(item)
    return session.commit()


def getItem(itemName, id):
    item = session.query(getClassByName(itemName)).filter_by(id=id).first()
    return item


def getClassByName(itemName):
    return entities.get(itemName)


def getPathByName(itemName):
    paths = {
        'puppy': 'puppies',
        'shelter': 'shelters',
        'owner': 'owners'
    }
    return paths.get(itemName)
