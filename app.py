import os.path
import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId 


app = Flask(__name__)
useMongo = True
if useMongo :
    client = MongoClient(r"mongodb://final200meters:zdYYRBK8jRehhhFDAY6ZPoWUnrUQodXZ7bWqTBqud492KliiiNsjBF66ZFURpI2Uctcmz08X9WcgVImB6BBJYg==@final200meters.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@final200meters@")
    db = client.mymongodb 
    heroescollection = db.heroescollection
    colticketmasterevents = db.ticketmasterevents
else :
    root_dir = os.path.dirname(__file__)

CORS(app)

def readHeroes() :
    if useMongo :
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

@app.route("/seedevents", methods=["GET"])
def seedevents():
    apiKey = 'cFaY8gBrFpniYpztVKtGGrVj4ShdD3pq'
    venueId = 'KovZ917AOAw'
    endpoint = 'https://app.ticketmaster.com/discovery/v2/'    
    tickmaster_url = endpoint + "events.json"
    headers = {}
    params = {'venueId': venueId, 'apikey': apiKey}
    response = requests.get(tickmaster_url, headers=headers, params=params, verify=False)
    response.raise_for_status()
    responsejson = response.json()
    events = responsejson["_embedded"]["events"]
    for event in events :
        status = event["dates"]["status"]["code"]
        if status == "onsale" :
            name = event["name"]
            id = event["id"]
            url = event["url"]
            startTime = event["dates"]["start"]["dateTime"]
            post = { "id":id, "name":name, "url":str(url)}
            if startTime :
                post["startTime"] = str(startTime)
            colticketmasterevents.insert_one(post).inserted_id
    #check the response to see how many reamining pages there are in the pagination
    #and call again for each page
    totalpages = responsejson["page"]["totalPages"]
    print(totalpages)
    if totalpages > 1:
        for i in range(1, totalpages):
            if i > 10 : 
                continue #lets set a hard limit of 10 requests
            params["page"] = i
            response = requests.get(tickmaster_url, headers=headers, params=params, verify=False)
            response.raise_for_status()
            responsejson = response.json()
            events = responsejson["_embedded"]["events"]
            for event in events :
                status = event["dates"]["status"]["code"]
                if status == "onsale" :
                    name = event["name"]
                    id = event["id"]
                    url = event["url"]
                    post = { "id":id, "name":name, "url":str(url)}
                    if "dateTime" in event["dates"]["start"].keys() :
                        startTime = event["dates"]["start"]["dateTime"]
                        post["startTime"] = str(startTime)
                    else :
                        post["startTime"] = "TBD"
                    colticketmasterevents.insert_one(post).inserted_id
    return jsonify({})

@app.route("/events", methods=["GET"])
def getEvents() :
    data = colticketmasterevents.find()
    events = []
    for item in data :
        events.append({"id":item["id"], "name":item["name"],"url":item["url"], "startTime":item["startTime"]})
    return jsonify(events)

@app.route("/events/<event_id>", methods=["GET"])
def getEvent(event_id=0):
    item = colticketmasterevents.find_one({"id": str(event_id)})
    event = {"id":item["id"], "name":item["name"],"url":item["url"], "startTime":item["startTime"]}
    return jsonify(event)


if __name__ == "__main__":
    if useMongo : 
        print("no files only mongo")
    else :
        #seed the heroes.json file with the template if it doesn"t exist
        if not os.path.exists(os.path.join(root_dir, "out", "heroes.json")):
            with open(os.path.join(root_dir, "out", "heroes-template.json"), "r") as templatefile:
                templatefiledata=templatefile.read()
            with open(os.path.join(root_dir, "out", "heroes.json"), "w") as newfile:
                newfile.write(templatefiledata)

    app.run(host="0.0.0.0", port=80)
