import os.path
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def readHeroesFile() :
    script_dir = os.path.dirname(__file__)
    print(script_dir)
    with open(script_dir + "/out/heroes.json", "r") as heroesfile:
        data=heroesfile.read()
    return json.loads(data)

def writeHeroesFile(heroesList) :
    script_dir = os.path.dirname(__file__)
    with open(script_dir + "/out/heroes.json", "w") as jsonFile:
            json.dump(heroesList, jsonFile)

# GET /heroes/{id} to return a specific Hero
@app.route("/heroes/<hero_id>", methods=["GET"])
def getHero(hero_id=0):
    heroesList = readHeroesFile()
    returnHero = {}
    for hero in heroesList:
        if int(hero["id"]) == int(hero_id) :
            returnHero = hero
    return jsonify(returnHero)

# GET /heroes to return all Heroes
@app.route("/heroes", methods=["GET"])
def getAllHero():
    heroesList = readHeroesFile()
    return jsonify(heroesList)

# POST /heroes to create a Hero
@app.route("/heroes", methods=["POST"])
def createHero():
    print("post createHero called")
    content_type = request.headers.get("Content-Type")
    if (content_type == "application/json"):
        jsonRequest = request.json
        heroesList = readHeroesFile()
        heroesList.append(jsonRequest)
        writeHeroesFile(heroesList)
        return jsonify({})
    else:
        return "Content-Type not supported!"

# PUT /heroes/{id} to modify a Hero
# DELETE /heroes/{id} to delete a Hero
# GET /heroes/search/name?contains={string} to search for Heroes
# GET /heroes/search/name?contains={string} to search for Heroes

if __name__ == "__main__":
    #seed the heroes.json file with the template if it doesn"t exist
    if not os.path.exists("out/heroes.json"):
        with open("out/heroes-template.json", "r") as templatefile:
            templatefiledata=templatefile.read()
        with open("out/heroes.json", "w") as newfile:
            newfile.write(templatefiledata)

    app.run(host="0.0.0.0", port=80)
    