import sys
from pymongo import MongoClient
import dbQuery

client = MongoClient()
db = client.db
coll = db.playerStorage
#result = db.playerStorage.delete_many({})

class PlayerStats:
	def __init__(self, name):
		'''Player class that stores cumulative stats'''
		self.name = name
		self.status = 1
		self.current = 1
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
						'current' : self.current,
						'stats' : self.stats}
		return playerDict

	def LoadFromDB(self, cursor):

		if cursor.count != 1:
			for document in cursor:
				self.status = document['status']
				self.stats = document['stats']
				self.current = document['current']

			return 1
		else:
			return 0

	def UpdateDB(self):
		result = db.playerStorage.update_one(
			{'name' : self.name},
			{'$set' : {'status' : self.status,
					'stats' : self.stats
					'current' : self.current}
			})
		return result



#Add in all players from the raw data into processed player storage 
playerCur = dbQuery.GetAllPlayers()

for player in playerCur:

	print player['_id']

	#Query the player
	cursor = coll.find({'name' : player['_id']})
	currentPlayer = PlayerStats(player['_id'])
	
	#If player is already in database
	if cursor.count() != 0:
		#read the player data
		currentPlayer.LoadFromDB(cursor)	
		gameList = dbQuery.GetPlayerGameList(currentPlayer.name)

		for gameID in gameList:
			if currentPlayer.current < gameID:
				#make changes to player HERE
				
				currentPlayer.stats['gp']  = currentPlayer.stats['gp'] + 1

				currentPlayer.current = gameID
				
				#then reinsert/update
				currentPlayer.UpdateDB


	#If player is not in the database
	elif cursor.count() == 0:
		#create the player
		currentPlayer = PlayerStats(player['_id'])
		#insert the player
		result = coll.insert_one(currentPlayer.OutputDict())

	
