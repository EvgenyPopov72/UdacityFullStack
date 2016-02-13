from flask import Flask, render_template, request, redirect, url_for
from puppies import app
from controllers import getItemsList, addNewItem, getItem, deleteExistingItem, getClassByName, getPathByName
from models import Base, Shelter, Puppy, Owner, entities
from dateutil import parser
from time import strftime
from datetime import datetime


@app.route('/')
def index():
    return render_template('layout.html')


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('pageNotFound.html')


@app.route('/puppies')
def listPuppies():
    return render_template('listPuppies.html', listOfItems=getItemsList(Puppy))


@app.route('/shelters')
def listShelters():
    return render_template('listShelters.html', listOfItems=getItemsList(Shelter))


@app.route('/owners')
def listOwners():
    return render_template('listOwners.html', listOfItems=getItemsList(Owner))


# @app.route('/puppy/new', methods=['GET', 'POST'])
# def newPuppy():
#     if request.method == 'POST':
#         if request.form['nameOfItem'] == 'puppy':
#             addNewItem(Puppy)
#         return redirect('/puppies')
#     return render_template('newItem.html', nameOfItem='puppy', actionPath=url_for('newPuppy'))

@app.route('/puppy/new', methods=['GET', 'POST'])
@app.route('/shelter/new', methods=['GET', 'POST'])
@app.route('/owner/new', methods=['GET', 'POST'])
def newEntityItem():
    entityName = request.base_url.split('/')[3]
    if request.method == 'POST':
        # TODO change ['puppy', 'shelter', 'owner']
        reqForm = request.form
        if reqForm['nameOfEntity'] in ['puppy', 'shelter', 'owner']:
            newItem = None
            if entityName == 'puppy':
                dateOfBirth = unicode(parser.parse(reqForm['dateOfBirth']).date().isoformat())
                # dateOfBirth = strftime('%Y-%m-%d', dateOfBirth)
                newItem = Puppy(name=reqForm['itemName'], gender=reqForm['puppyGender'],
                                dateOfBirth=dateOfBirth, picture=reqForm['puppyPicture'],
                                weight=reqForm['puppyWeight'])
            elif entityName == 'shelter':
                newItem = Shelter(name=reqForm['itemNAme'], address=reqForm['shelterAddress'],
                                  city=reqForm['shelterCity'], zipCode=reqForm['shelterZip'],
                                  state=reqForm['shelterState'], website=reqForm['shelterURL'])
            addNewItem(newItem)
        # TODO change redirect
        return redirect(getPathByName(entityName))
    return render_template('newItem.html', nameOfEntity=entityName)


# @app.route('/puppy/<int:id>/delete', methods=['GET', 'POST'])
# @app.route('/shelter/<int:id>/delete', methods=['GET', 'POST'])
@app.route('/<string:entityName>/<int:id>/delete', methods=['GET', 'POST'])
def deleteItem(entityName, id):
    item = getItem(entityName, id)
    if request.method == 'POST':
        if request.form['nameOfItem'] == item.name:
            deleteExistingItem(item)
        return redirect(getPathByName(entityName))
    return render_template('deleteWarning.html', Item=item,
                           actionPath=url_for('deleteItem', entityName=entityName, id=id))
