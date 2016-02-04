from pymongo import MongoClient
import sys

#Test bed for queries on database
client = MongoClient()
db = client.db
coll = db.test

# cursor = db.test.find({"pbp.eventType" : "GOAL"}, 
# 					{"pbp.$" : 1})


# cursor = db.test.find({"pbp": {"$elemMatch": {
# 							"eventType": "GOAL",
# 							"period": "2"
# 	}}}, 
# 					{"pbp.$" : 1})
#cursor = db.test.find({"pbp.eventType" : "GOAL"} , {"pbp" : {"$slice" : 2}})



# cursor = db.test.aggregate([
# 	{"$match" : {"pbp.period" : "2"}},
# 	{
# 		"$project": {
# 			"pbp": {
# 				"$filter": {"input" : "$pbp", "as": "item","cond": {"$$item.eventType" : "GOAL"}
# 				}
# 			}
# 		}
# 	}])

def CountEventTypes():
	'''Provides counts for the number of events that happened'''
	#To Do provide filtering via $match or w/e
	cursor = db.test.aggregate([
		{"$match" : {}},
		{"$unwind" : "$pbp"},
		{"$group" : {"_id" : "$pbp.eventType",
					"count" : {"$sum" : 1}
					}}
		])

	return cursor

def GetAllPlayers():
	'''Grab all players in database'''
	cursor = db.test.aggregate([
		{"$match" : {}},
		{"$unwind" : "$pbp"},
		{"$project" : {"players" : {"$setUnion" : ["$pbp.homeTeam" , "$pbp.awayTeam"]}}},
		{"$unwind" : "$players"},
		{"$group":{"_id" : "$players",
					"count" : {"$sum" : 1}}}

		])

	return cursor

def GetPlayerGameList(player):
	'''Find the latest game that the player was involved in'''
	cursor = db.test.aggregate([
		{"$match" : {}},
		{"$unwind" : "$pbp"},
		{"$match" : {"$or" : [{"pbp.homeTeam" : str(player)}, {"pbp.awayTeam" : str(player)}]}},
		{"$group":{"_id" : "$game_id",
					"count" : {"$sum" : 1}}}

		])
	return cursor


def PBPPlayerQuery(player):
	'''Returns events when a player was on the ice'''
	#
	cursor = db.test.aggregate([
		{"$match" : {}},
		{"$unwind" : "$pbp"},
		{"$match" : {"$or" : [{"pbp.homeTeam" : str(player)}, {"pbp.awayTeam" : str(player)}]}},
		{"$project" : {
						"game_id" : "$game_id",
						"playId" : "$pbp.playId",
						"period" : "$pbp.period",
						"timeInPeriod" : "$pbp.timeInPeriod",
						"homeTeamStatus" : "$pbp.homeTeamStatus",
						"awayTeamStatus" : "$pbp.awayTeamStatus",
						"eventType" : "$pbp.eventType", 
						"desc" : "$pbp.desc",
						"home" : "$pbp.homeTeam",
						"away" : "$pbp.awayTeam"}}])
		
	return cursor	

# test = PBPPlayerQuery("MARC STAAL")
# for thing in test:
# 	print thing["desc"]
# sys.exit()

def PBPGameQuery(game, period, eventType):
	'''Returns list of plays in a period with a certain event for a particular game'''
	#http://stackoverflow.com/questions/3985214/retrieve-only-the-queried-element-in-an-object-array-in-mongodb-collection
	#First match will filter by game
	#Match is the criteria
	cursor = db.test.aggregate([
		{"$match" : {"game_id" : str(game)}},
		{"$unwind" : "$pbp"},
		{"$match" : {"pbp.eventType" : str(eventType),
					"pbp.period" : str(period) }},
		{"$project" : {
						"game_id" : "$game_id",
						"playId" : "$pbp.playId",
						"period" : "$pbp.period",
						"timeInPeriod" : "$pbp.timeInPeriod",
						"homeTeamStatus" : "$pbp.homeTeamStatus",
						"awayTeamStatus" : "$pbp.awayTeamStatus",
						"eventType" : "$pbp.eventType", 
						"desc" : "$pbp.desc",
						"home" : "$pbp.homeTeam",
						"away" : "$pbp.awayTeam"}}])
		
	return cursor	

def ESGamePlayerQuery(game, player):
	#cursor = db.eventSummary.find({"game_id" : "201420150078"})
	#PLAYER NAME IS lke KUCHEROV, NIKITA IN THE DATABASE
	cursor = db.eventSummary.aggregate([
		{"$match" : {"game_id" : str(game)}},
		{"$project" : {"players" : {"$setUnion" : ["$homePlayers" , "$awayPlayers"]}}},
		{"$unwind" : "$players"},
		{"$match" : {"players.name" : str(player)}},
		{"$project" : {
					"jersey" : "$players.name"
		}}
	])

	return cursor


def main():
	test = PBPGameQuery("201420150005",1, "GOAL")
	test = PBPPlayerQuery("PATRICK MARLEAU")
	test = GetPlayerGameList("PATRICK MARLEAU")
	test = ESGamePlayerQuery("201420150078", "KUCHEROV, NIKITA")
	for thing in test:
		for key in thing.keys():
			print "--" +  key
			print thing[key]
			print type(thing[key])


	sys.exit()

if __name__ == "__main__":
    main()
# cursor = db.test.aggregate([
# 	{"$match" : {"pbp.period" : "2"}},
# 	{"$unwind" : "$pbp"},
# 	{"$match" : {"pbp.eventType" : "GOAL"}},
# 	{"$project" : {"item" : "$pbp.eventType", 
# 					"id" : "$pbp.playId",
# 					"home" : "$pbp.homeTeam",
# 					"away" : "$pbp.awayTeam"}
	

# 	])
	

# for document in cursor:
# 	print (document["home"])
