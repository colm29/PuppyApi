from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy


engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

app = Flask(__name__)


def newSession():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


@app.route("/")
@app.route("/puppies", methods=['GET', 'POST'])
def puppiesFunction():
    if request.method == 'GET':
        return getAllPuppies()
    elif request.method == 'POST':
        print("Making a New puppy")

        name = request.args.get('name', '')
        description = request.args.get('description', '')
        print(name)
        print(description)
        return makeANewPuppy(name, description)


# Make another app.route() decorator here that takes in an integer id in the URI
@app.route("/puppies/<int:id>", methods=['GET', 'PUT', 'DELETE'])
# Call the method to view a specific puppy
def puppiesFunctionId(id):
    if request.method == 'GET':
        return getPuppy(id)

# Call the method to edit a specific puppy
    elif request.method == 'PUT':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return updatePuppy(id, name, description)

     # Call the method to remove a puppy
    elif request.method == 'DELETE':
        return deletePuppy(id)


def getAllPuppies():
    session = newSession()
    try:
        puppies = session.query(Puppy).all()
        return jsonify(Puppies=[i.serialize for i in puppies])
    finally:
        session.close()


def getPuppy(id):
    session = newSession()
    try:
        puppy = session.query(Puppy).filter_by(id=id).one()
        return jsonify(puppy=puppy.serialize)
    finally:
        session.close()


def makeANewPuppy(name, description):
    session = newSession()
    try:
        puppy = Puppy(name=name, description=description)
        session.add(puppy)
        session.commit()
        return jsonify(Puppy=puppy.serialize)
    finally:
        session.close()


def updatePuppy(id, name, description):
    session = newSession()
    try:
        puppy = session.query(Puppy).filter_by(id=id).one()
        if not name:
            puppy.name = name
        if not description:
            puppy.description = description
        session.add(puppy)
        session.commit()
        return "Updated a Puppy with id %s" % id
    finally:
        session.close()


def deletePuppy(id):
    session = newSession()
    try:
        puppy = session.query(Puppy).filter_by(id=id).one()
        session.delete(puppy)
        session.commit()
        return "Removed Puppy with id %s" % id
    finally:
        session.close()


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
