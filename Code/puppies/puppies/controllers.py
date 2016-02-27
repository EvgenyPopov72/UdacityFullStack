from models import entities, session


def getItemsList(items, filterParam=''):
    # TODO add check for sql injection
    if filterParam:
        return session.query(items).filter(items.name.like('%'+filterParam+'%')).order_by(items.name).all()
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
