"""
Author: Meixian Chen

run the following command before the statistic:

mongoimport --db sample --collection sulishi --drop --file ../data/clean.json

"""

import json
from pymongo import MongoClient
from pprint import pprint


def get_one(db):
    print "a document from the data"
    pprint(db.sulishi.find_one())

def get_db():
    client = MongoClient("localhost:27017")
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.sample
    return db

def overview(db):
    print "Number of documents"
    print db.sulishi.find().count()

    print "Number of nodes"
    print db.sulishi.find({"type":"node"}).count()

    print "Number of ways"
    print db.sulishi.find({"type":"way"}).count()

    print "Number of unique users"
    print len(db.sulishi.distinct("created.uid"))

    print "Top 5 contributing users"
    res= db.sulishi.aggregate([{"$match":{"created.user":{"$exists":1}}},
    {"$group":{"_id":"$created.user","count":{"$sum":1}}},
    {"$sort":{"count":-1}},{"$limit":5}])
    results = [doc for doc in res]
    pprint(results)


def amenity(db):
    print "Number of amenities"
    #print db.sulishi.aggregate([{"$match":{"amenity":{"$exists":1}}}]).count()
    print db.sulishi.find({"amenity":{"$exists":1}}).count()

    print "Top 20 amenities"
    res = db.sulishi.aggregate([{"$match":{"amenity":{"$exists":1}}},
    {"$group":{"_id":"$amenity","count":{"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":20}
    ])
    pprint([doc for doc in res])

def popular_cusine(db):

    print "Top 10 cusine"
    res = db.sulishi.aggregate([{"$match":{"cuisine":{"$exists":1}}},
    {"$group":{"_id":"$cuisine","count":{"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":10}
    ])
    pprint([doc for doc in res])

def recycling(db):

    print "recycling place"
    res = db.sulishi.aggregate([{"$match":{"recycling_type":{"$exists":1}}},
    {"$group":{"_id":"$recycling_type","count":{"$sum":1}}},
    {"$sort":{"count":1}},
    {"$limit":5}
    ])
    pprint([doc for doc in res])

    print "top 5 items with the fewest recycling spot"
    res = db.sulishi.aggregate([{"$match":{"recycling":{"$exists":1}}},
    {"$unwind":"$recycling"},
    {"$group":{"_id":"$recycling","count":{"$sum":1}}},
    {"$sort":{"count":1}},
    {"$limit":5}
    ])
    pprint([doc for doc in res])

    print "top 5 items with the most recycling spot"
    res = db.sulishi.aggregate([{"$match":{"recycling":{"$exists":1}}},
    {"$unwind":"$recycling"},
    {"$group":{"_id":"$recycling","count":{"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":5}
    ])
    pprint([doc for doc in res])

def tourism(db):
    print "Top 10 tourist place"
    res = db.sulishi.aggregate([{"$match":{"tourism":{"$exists":1}}},
    {"$group":{"_id":"$tourism","count":{"$sum":1}}},
    {"$sort":{"count":-1}},
    {"$limit":10}
    ])
    pprint([doc for doc in res])


if __name__ == "__main__":
    # For local use
    db = get_db() # uncomment this line if you want to run this locally

    get_one(db)
    overview(db)
    amenity(db)
    popular_cusine(db)
    tourism(db)
    recycling(db)
