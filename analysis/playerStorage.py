import sys
from pymongo import MongoClient
import readDataTest

client = MongoClient()
db = client.db
coll = db.playerStorage
#result = db.playerStorage.delete_many({})

class PlayerStats:
	def __init__(self, name):
		'''Player class that stores cumulative stats'''
		self.name = name
		self.status = 1

		self.stats = ({'team' : "",
							'gp' : 1,
							'goals' : 0,
							'assists' : 0,
							'plusMinus' : 0
							})

	def OutputDict(self):
		'''Output as a dictionary to insert into database'''
		playerDict = {'name' : self.name,
						'status' : self.status,
						'stats' : self.stats}
		return playerDict

	def LoadFromDB(self, cursor):

		if cursor.count != 1:
			for document in cursor:
				self.status = document['status']
				self.stats = document['stats']

			return 1
		else:
			return 0



#Add in all players from the raw data into processed player storage 
playerCur = readDataTest.GetAllPlayers()

for player in playerCur:

	print player['_id']
	#Query the player
	cursor = coll.find({'name' : player['_id']})

	currentPlayer = PlayerStats(player['_id'])
	
	#If player is already in database
	if cursor.count() != 0:
		#read the player data
		currentPlayer.LoadFromDB(cursor)	

		#make changes to player HERE
		currentPlayer.stats['gp']  = 2

		#then reinsert/update
		result = db.playerStorage.update_one(
			{'name' : player['_id']},
			{'$set' : {'status' : currentPlayer.status,
						'stats' : currentPlayer.stats}
			})


	#If player is not in the database
	elif cursor.count() == 0:
		#create the player
		currentPlayer = PlayerStats(player['_id'])
		#insert the player
		result = coll.insert_one(currentPlayer.OutputDict())

	
