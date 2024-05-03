from pymongo import MongoClient
from pprint import pprint

print("running")
client = MongoClient(open("./secrets/mongoDB", "r").read())

print("check 1")

restaurant = {
    "name": "The Spire",
    "address": "Dublin",
    "location": {
        "type": "Point",
        "coordinates": [-6.260251824915252, 53.34981854814901] #Long Lat
    },
    "tags": ["american", "burgers"],
    "desc": "A modern New American burger joint. Has a cool metal pole"
}

print("check 2")

database = client.idp11_data
print("check 3")

restaurants = database.restaurants
print("check 4")

if input("do you want to insert the spire?") == "true":
    post_id = restaurants.insert_one(restaurant).inserted_id
    restaurants.create_index( { "location" : "2dsphere" } )
    print("done")

nearLocations = restaurants.find(
    {
        "location":{
            "$near" : {
                "$geometry": {"type": "Point", "coordinates": [-6.267802070352944, 53.349406567892196]},
                "$minDistance": 0,
                "$maxDistance": 5000
            }
        }
    }
)

print(nearLocations)

for doc in nearLocations:
    print(doc["name"])
    print("iterated")