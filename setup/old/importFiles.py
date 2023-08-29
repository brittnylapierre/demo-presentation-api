import couchdb
import json
import os

couch = couchdb.Server("http://admin:YOURPASSWORD@localhost:5984/")

db = couch["manifest"]

path = "./manifests"
dir = os.listdir( path )

for file in dir:
    try:
        with open("./manifests/" + file) as jsonfile:
            db_entry = json.load(jsonfile)
            db.save(db_entry)
    except Exception as e: print(e)