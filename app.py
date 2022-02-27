from crypt import methods
from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/getmap/', methods=['GET', 'POST'])
def getmap():
    return jsonify({'id':'1234','name':'Gabba Gabba Hey', 'venue':'Madison Square Garden', 'performer':"Ramones", "when":"16MAY1993"})


# GET /heroes/{id} to return a specific Hero
@app.route('/heroes/<hero_id>', methods=['GET'])
def getHero(hero_id=0):
    print("The hero id is " + str(hero_id))
    return jsonify({})

# GET /heroes to return all Heroes
@app.route('/heroes/', methods=['GET'])
def getAllHero():
    print("get all heroes called")
    return jsonify({})

# POST /heroes to create a Hero
@app.route('/heroes/', methods=['POST'])
def createHero():
    print("post createHero called")
    return jsonify({})

# PUT /heroes/{id} to modify a Hero
@app.route('/heroes/<hero_id>', methods=['PUT'])
def modifyHero(hero_id=0):
    print("modify hero " + str(hero_id))
    return jsonify({})

# DELETE /heroes/{id} to delete a Hero
@app.route('/heroes/<hero_id>', methods=['DELETE'])
def deleteHero(hero_id=0):
    print("delete hero " + str(hero_id))
    return jsonify({})

# GET /heroes/search/name?contains={string} to search for Heroes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)