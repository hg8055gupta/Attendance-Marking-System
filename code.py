from pymongo import MongoClient
import pprint
client = MongoClient('localhost', 27017)
db = client.test
posts = db.posts
#pprint.pprint(posts.find_one())
posts.insert_one({"dict":["dd"]})
posts.drop()
data = posts.find()
set_items = set(data['names'])
#print(data['names'])
#posts.find_one_and_update({}, {"$set":{'names':data['names']+['harsh']}}, upsert=True)
#data = posts.find_one()
#print(set_items)