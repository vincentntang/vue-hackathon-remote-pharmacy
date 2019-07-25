from pymongo import MongoClient
import json
from bson.json_util import dumps

cluster = MongoClient("MONGO STRING URI HERE")
db = cluster["remotepharmacy"]
db2 = cluster["radose"]

live = db2.live
hist = db2.historical

myquery = { "userid": "1" }
newvalues = { "$set": { "data": ["21","29","89","14","18","17","19"] } }

result = live.update_one(myquery, newvalues, upsert=True)

##res = live.update()

# for x in live.find():
#   print(x)
#   ##print (x['userid'])
#   if x['userid'] =='1':
#        print("found")
#        out = dumps(x)
#        break

# print (out)


vals =  '{"prescriptionID": "29","patientID" : "1", "medicationName": "Vicodin", "dosage": "B", "refillable": "0"}'
data = json.loads(vals)
prescriptions = db.prescriptions

prescriptions.insert_one(data)