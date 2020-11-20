import recommender
import pandas as pd
from pymongo import MongoClient
import redis

client = MongoClient('mongodb://localhost:27017/')
# data base name : testDB
mydb = client['test1DB']
training_data = pd.read_csv("final_songs.csv",encoding = 'unicode_escape')

model = recommender.item_similarity_recommender()
model.create(training_data,'user_id','name')
df = model.get_similar_items(['Breakdown - Jack Johnson', 'Invalid - Tub Ring'])
data={}
for i,r in df.iterrows():
    print(r["song"],r["rank"])
    row={}
    row["song"]=r["song"]
    row["rank"]=r["rank"]
    data[i]=row
    #mydb.RecommendedSongs.insert_one(row)
r = redis.Redis(host="localhost",port=6379,db=0)
#print(data)
r.set("recent-songs",str(data))
print('done')