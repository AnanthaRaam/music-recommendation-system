
import pandas as pd
#import  numpy as np
import os
import csv
import redis

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# data base name : 'testDB'
mydb = client['testDB']

# reading data from file
song_data_1 = pd.read_table("triplets.txt",header=None,names=['user_id','song_id','listen_count'])
song_data_2 = pd.read_csv("song_data.csv")

#print(len(song_data_1))

#selecting 1% of entire data with shuffling due to space constraints
song_data_1 = song_data_1.sample(frac=0.01,random_state=2)
#print(len(song_data_1))

# consider users who lisened more than 5 songs useful for item item filtering
song_data_1.groupby(['user_id']).filter(lambda x: len(x) > 5)

# merge two dataframes 
songs = pd.merge(song_data_1, song_data_2.drop_duplicates(['song_id']), on='song_id', how='left')

#print(len(songs))

def full_name(title, artist):
    return (title + ' - ' + artist)

# merge title and artists        
songs['name'] = songs.apply(lambda x: full_name(x['title'], x['artist_name']), axis=1)

#print(songs['name'])

# group song dataset by number of listen_count in ascending order
# calculate the entire listen count for each song
# create percentage column

songs_grouped = songs.groupby(['name']).agg({'listen_count': 'count'}).reset_index()
total_listens = songs_grouped['listen_count'].sum()
songs_grouped['percentage']  = songs_grouped['listen_count'].div(total_listens)*100
songs_final = songs_grouped.sort_values(by='percentage', ascending=False)

#print(songs_final)

folder = os.getcwd()
songs.to_csv(folder+"\\final_songs.csv")
"""
csvfile = open(folder+"\\final_songs.csv", 'r')
reader = csv.DictReader(csvfile)
header = ["name","listen_count","percentage"]
for each in reader:
    row={}
    for field in header:
        row[field]=each[field]
    mydb.songs.insert_one(row)
    
data = {
"1": {"song_id": "sample1","listen_count": 5,"user_id": "sampleu1"},
"2": {"song_id": "sample2","listen_count": 2,"user_id": "sampleu2"},
"3": {"song_id": "sample3","listen_count": 3,"user_id": "sampleu3"},
"4": {"song_id": "sample4","listen_count": 4,"user_id": "sampleu4"},
"5": {"song_id": "sample5","listen_count": 5,"user_id": "sampleu5"}  
}
r = redis.Redis(host="localhost",port=6379,db=0)
r.set("recent-songs",str(data))
"""
print("done")