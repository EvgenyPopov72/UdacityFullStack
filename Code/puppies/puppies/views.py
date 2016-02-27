from flask import Flask, render_template, request, redirect, url_for
from puppies import app
from controllers import getItemsList, addUpdateItem, getItem, deleteExistingItem, getClassByName, getPathByName
from models import Base, Shelter, Puppy, Owner, entities
from dateutil import parser

entytiesList = ['puppy', 'shelter', 'owner']


@app.route('/')
def index():
    return render_template('layout.html')


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('pageNotFound.html')


@app.route('/puppies')
def listPuppies():
    filterString = request.args.get('filter')
    return render_template('listPuppies.html', listOfItems=getItemsList(Puppy, filterString))


@app.route('/shelters')
def listShelters():
    filterString = request.args.get('filter')
    return render_template('listShelters.html', listOfItems=getItemsList(Shelter, filterString))


@app.route('/owners')
def listOwners():
    filterString = request.args.get('filter')
    return render_template('listOwners.html', listOfItems=getItemsList(Owner, filterString))


# @app.route('/puppy/new', methods=['GET', 'POST'])
# @app.route('/shelter/new', methods=['GET', 'POST'])
@app.route('/<string:entityName>/new', methods=['GET', 'POST'])
def newEntityItem(entityName):
    if entityName not in entytiesList:
        return redirect('/')
    if request.method == 'POST':
        reqForm = request.form
        if reqForm['nameOfEntity'] in entytiesList:
            newItem = None
            if entityName == 'puppy':
                dateOfBirth = parser.parse(reqForm['dateOfBirth']).date().isoformat()
                weight = reqForm['puppyWeight'] if len(reqForm['puppyWeight']) > 0 else 0
                newItem = Puppy(name=reqForm['itemName'], gender=reqForm['puppyGender'],
                                dateOfBirth=dateOfBirth, picture=reqForm['puppyPicture'],
                                weight=weight, shelter_id=reqForm['puppyShelter'])
            elif entityName == 'shelter':
                newItem = Shelter(name=reqForm['itemName'], address=reqForm['shelterAddress'],
                                  city=reqForm['shelterCity'], zipCode=reqForm['shelterZip'],
                                  state=reqForm['shelterState'], website=reqForm['shelterURL'])
            elif entityName == 'owner':
                newItem = Owner(name=reqForm['itemName'], address=reqForm['ownerAddress'])

            addUpdateItem(newItem)
        return redirect(getPathByName(entityName))
    # return render_template('newItem.html', nameOfEntity=entityName, shelters=getItemsList(Shelter), item=None)
    return render_template('editItem.html', nameOfEntity=entityName, shelters=getItemsList(Shelter), item=None,
                           operation='new')


@app.route('/<string:entityName>/<int:id>/edit', methods=['GET', 'POST'])
def editEntityItem(entityName, id):
    if entityName not in entytiesList:
        return redirect('/')
    item = getItem(entityName, id)
    if request.method == 'POST':
        reqForm = request.form
        if reqForm['nameOfEntity'] in entytiesList:
            item.name = reqForm['itemName']
            if entityName == 'puppy':
                item.gender = reqForm['puppyGender']
                item.dateOfBirth = parser.parse(reqForm['dateOfBirth']).date().isoformat()
                item.picture = reqForm['puppyPicture']
                item.weight = reqForm['puppyWeight'] if len(reqForm['puppyWeight']) > 0 else 0
                item.shelter_id = reqForm['puppyShelter']

            elif entityName == 'shelter':
                item.address = reqForm['shelterAddress']
                item.city = reqForm['shelterCity']
                item.zipCode = reqForm['shelterZip']
                item.state = reqForm['shelterState']
                item.website = reqForm['shelterURL']
            elif entityName == 'owner':
                item.address = reqForm['ownerAddress']

            addUpdateItem(item)
        return redirect(getPathByName(entityName))
    return render_template('editItem.html', nameOfEntity=entityName, item=item, shelters=getItemsList(Shelter))


@app.route('/<string:entityName>/<int:id>/delete', methods=['GET', 'POST'])
def deleteItem(entityName, id):
    if entityName not in entytiesList:
        return redirect('/')
    item = getItem(entityName, id)
    if request.method == 'POST':
        if request.form['nameOfItem'] == item.name:
            deleteExistingItem(item)
        return redirect(getPathByName(entityName))
    return render_template('deleteWarning.html', Item=item,
                           actionPath=url_for('deleteItem', entityName=entityName, id=id))
