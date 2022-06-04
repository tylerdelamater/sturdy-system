import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


app = Flask(__name__)
keyVaultName = 'sturdysystem-kv'
KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
kv = SecretClient(vault_url=KVUri, credential=credential)
connectionString = kv.get_secret('mongodbconnectionstring')
client = MongoClient(connectionString.value)
db = client.mymongodb 
colticketmasterevents = db.ticketmasterevents

CORS(app)

@app.route("/seedevents", methods=["GET"])
def seedevents():
    apikey = kv.get_secret('tmapikey').value
    venueId = 'KovZ917AOAw'
    endpoint = 'https://app.ticketmaster.com/discovery/v2/'    
    tickmaster_url = endpoint + "events.json"
    headers = {}
    params = {'venueId': venueId, 'apikey': apikey}
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
    app.run(host="0.0.0.0", port=8080)
