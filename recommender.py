import numpy as np
import pandas

class item_similarity_recommender():
    
    def __init__(self):
        self.training_data = None
        self.userid = None
        self.itemid = None
        self.cooccurence_matrix = None
        self.item_similarity_recommendation = None
    
    # create item item based recommender model
    def create(self,training_data,user_id,item_id):
        self.training_data = training_data
        self.userid = user_id
        self.itemid = item_id
    
    # get all unique users list for a given item ( song )
    def get_items_user(self,item):
        item_data = self.training_data[self.training_data[self.itemid] == item]
        items_user = set(item_data[self.userid].unique())
        return items_user
        
    # construct coccurence matrix
    def construct_cooccurence_matrix(self,user_given_songs,all_unique_songs):
        
        # get the user list who listened user given songs
        user_for_user_given_songs = []
        for i in range(0,len(user_given_songs)):
            user_for_user_given_songs.append(self.get_items_user(user_given_songs[i]))
        
        # initialise the matrix for len(user_given_songs)X len(all_unique_songs)
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_given_songs),len(all_unique_songs))),float)
        
        # fill cooccurence matrix
        for i in range(len(all_unique_songs)):
            
            # calculate no of unique listeners of all_unique_songs
            
            songs_i_data = self.training_data[self.training_data[self.itemid] == all_unique_songs[i]]
            user_i = set(songs_i_data[self.userid].unique())
            
            for j in range(0,len(user_given_songs)):
                
                # get all unique listeners of song j
                user_j = user_for_user_given_songs[j]

                # calculate the no of user who listened both songs i and j
                user_intersection = user_i.intersection(user_j)
                
                # calculate c[i,j] based on jaccard similarity
                
                if( len(user_intersection)!=0 ):
                    # calculate union of songs
                    user_union = user_i.union(user_j)
                    cooccurence_matrix[j,i] = float(len(user_intersection)/float(len(user_union)))
                else:
                    cooccurence_matrix[j,i]=0

        return cooccurence_matrix
                    
    # recommend songs
    def generate_top_songs(self,cooccurence_matrix,all_songs,user_songs):
        
        # calculate avg value for all songs in user given songs list
        user_songs_score = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
        user_songs_score = np.array(user_songs_score)[0].tolist()
        
        # sort indices of score list based on their value and maintain a list
        sort_i = sorted(((e,i) for i,e in enumerate(list(user_songs_score))),reverse=True)
        
        # create df
        
        columns = ['song','rank']
        df = pandas.DataFrame(columns=columns)
        
        # fill df with top 10 items
        rank=1
        for i in range(0,len(sort_i)):
            if(~np.isnan(sort_i[i][0]) and all_songs[sort_i[i][1]] not in user_songs and rank <= 10):
                df.loc[len(df)]=[all_songs[sort_i[i][1]],rank]
                rank = rank+1
        
        if(df.shape[0]==0):
            print("the current songs has no recommendation")
            return -1
        else:
            return df
            
    # get items similar to given input item list
    def get_similar_items(self,item_list):
        
        user_given_songs = item_list
        
        # get number of unique songs in the entire training data
        all_unique_songs = list(self.training_data[self.itemid].unique())
        print("searching the best songs for you among %d"%len(all_unique_songs))
        
        # construct cooccurence matrix for len(user_given_songs)Xlen(all_unique_songs)
        cooccurence_matrix = self.construct_cooccurence_matrix(user_given_songs,all_unique_songs)
        
        # use cooccrence matrix to generate recommendations
        
        df_recommendations = self.generate_top_songs(cooccurence_matrix,all_unique_songs,user_given_songs)
        return df_recommendations
