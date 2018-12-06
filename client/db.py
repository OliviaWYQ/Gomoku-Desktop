import pymongo
import time

class MongoClient:
    
    # to connect mongodb
    uri = None
    client = None
    cols = None
    
    # player info
    # win rate and related
    win_rate = None
    total_matches = None
    win_matches = None
    
    def __init__(self, uri="mongodb://longname:1longpass@ds143603.mlab.com:43603/ase"):
        self.uri = uri
        self.link()
    
    def link(self):
        self.client = pymongo.MongoClient(self.uri)
        self.cols = self.client.get_database()
        
    def insert_one_history(self, moves, black_win, user1_id, user2_id="LocalMode"):
        
        timestamp = int(time.time()*1000.0)
        match_id = user1_id + '#' + user2_id + str(timestamp)
        
        moves_encoded = self.moves_encode(moves)
        
        self.cols['history'].insert_one({
            "user_1": user1_id,
            "user_2": user2_id,
            "match_id": match_id, 
            "moves": moves_encoded,  
            "user1win": black_win})
    
    def moves_encode(self, moves):
        ms = []
        for m in moves:
            ms.append(m[0] | (m[1] << 8))
        return ms
    
    def moves_decode(self, moves):
        ms = []
        for m in moves:
            ms.append((m&255, m>>8))
        return ms
    
    def get_matches(self, user_id):
        cursor = self.cols['history'].find({'user_1': user_id})
        matches = []
        for m in cursor:
            matches.append(m)
        return matches
    
    def shut_down(self):
        self.client.close()
    
    def get_all_info(self, user_id):
        self.total_matches = self.cols['history'].count_documents({
            '$or':[
                {'user_1':user_id}, {'user_2':user_id}
            ]
        })
        self.win_matches = self.cols['history'].count_documents({
            '$or':[
                {'user_1':user_id, 'user1win': True}, {'user_2':user_id, 'user1win': False}
            ]
        })
        self.win_rate = (self.win_matches + 0.0) / self.total_matches
        return self.win_rate


# How to use
if __name__ == '__main__':

    client = MongoClient()

    # insert a match
    # the first player wins
    moves = [(1,2), (3,5), (7,9)]
    user1win = True
    user1_id = "testuser1"
    client.insert_one_history(moves, user1win, user1_id)
    # the second player wins
    moves = [(3,2), (3,5), (7,9)]
    user2win = False
    user2_id = "testuser2"
    client.insert_one_history(moves, user2win, user2_id)

    # get all matches by user id
    cursor = client.get_matches("testuser1")
    # display the matches
    for c in cursor:
        print(c)

    client.shut_down()