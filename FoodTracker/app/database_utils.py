from pymongo import MongoClient
import datetime as dt

TEAM_NAME = 'FOOD_APP';

def get_collection():
    return MongoClient()[TEAM_NAME].articles

def insert_submission(single_sub):
    coll = get_collection();
    existing = coll.find_one({"Email" : single_sub["Email"]});
    if existing is not None:
        print "We already have this user registered"
    else:
        print "inserting ->", single_sub
        coll.insert(single_sub);
    
    return True;


    

    
