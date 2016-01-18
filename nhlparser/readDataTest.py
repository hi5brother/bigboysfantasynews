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

def PBPTeamQuery():
	'''Returns events for a team'''

	pass

def PBPPlayerQuery(player):
	'''Returns events when a player was on the ice'''
	#
	cursor = db.test.aggregate([
		{"$match" : {}},
		{"$unwind" : "$pbp"},
		{"$match" : {"$or" : [{"pbp.homeTeam" : str(player)}, {"pbp.awayTeam" : str(player)}]}},
		{"$project" : {
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

test = PBPPlayerQuery("MARC STAAL")
for thing in test:
	print thing["desc"]
sys.exit()
def PBPGameQuery(game,period, eventType):
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

test = PBPQuery("201420150001",1, "GOAL")
for thing in test:
	for key in thing.keys():
		print thing[key]

test = db.test.find()

sys.exit()


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
