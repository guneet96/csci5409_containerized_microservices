import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["travel_app"]
my_collec = mydb["places"]

for i in range(10):
	


