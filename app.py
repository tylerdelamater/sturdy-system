import os.path
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
prod = False
if os.getenv("APP_PATH") :
    prod = True
    client = MongoClient(r"mongodb://final200meters:zdYYRBK8jRehhhFDAY6ZPoWUnrUQodXZ7bWqTBqud492KliiiNsjBF66ZFURpI2Uctcmz08X9WcgVImB6BBJYg==@final200meters.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@final200meters@")
    db = client.mymongodb 
    heroescollection = db.heroescollection 
else :
    root_dir = os.path.dirname(__file__)

CORS(app)

def readHeroes() :
    if prod :
        data = heroescollection.find()
        print(type(data))
        print(dir(data))
        heroesList = []
        for item in data :
            heroesList.append({"id":item["id"], "name":item["name"]})
        return heroesList
    else :   
        print(os.path.join(root_dir, "out", "heroes.json"))
        with open(os.path.join(root_dir, "out", "heroes.json"), "r") as heroesfile:
            data=heroesfile.read()
        return json.loads(data)

def writeHeroes(heroesList) :
    with open(os.path.join(root_dir, "out", "heroes.json"), "w") as jsonFile:
            json.dump(heroesList, jsonFile)

# GET /heroes/{id} to return a specific Hero
@app.route("/heroes/<hero_id>", methods=["GET"])
def getHero(hero_id=0):
    heroesList = readHeroes()
    returnHero = {}
    for hero in heroesList:
        if int(hero["id"]) == int(hero_id) :
            returnHero = hero
    return jsonify(returnHero)

# GET /heroes to return all Heroes
@app.route("/heroes", methods=["GET"])
def getAllHero():
    heroesList = readHeroes()
    return jsonify(heroesList)

# POST /heroes to create a Hero
@app.route("/heroes", methods=["POST"])
def createHero():
    print("post createHero called")
    content_type = request.headers.get("Content-Type")
    if (content_type == "application/json"):
        jsonRequest = request.json
        heroesList = readHeroes()
        heroesList.append(jsonRequest)
        writeHeroes(heroesList)
        return jsonify({})
    else:
        return "Content-Type not supported!"

# PUT /heroes/{id} to modify a Hero
# DELETE /heroes/{id} to delete a Hero
# GET /heroes/search/name?contains={string} to search for Heroes
# GET /heroes/search/name?contains={string} to search for Heroes

if __name__ == "__main__":
    if prod : 
        print("no files only mongo")
    else :
        #seed the heroes.json file with the template if it doesn"t exist
        if not os.path.exists(os.path.join(root_dir, "out", "heroes.json")):
            with open(os.path.join(root_dir, "out", "heroes-template.json"), "r") as templatefile:
                templatefiledata=templatefile.read()
            with open(os.path.join(root_dir, "out", "heroes.json"), "w") as newfile:
                newfile.write(templatefiledata)

    app.run(host="0.0.0.0", port=80)
    