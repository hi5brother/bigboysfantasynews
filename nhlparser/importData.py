from pymongo import MongoClient
import json, bson
import parser_pbp
import parser_event_summary
import sys


'''
when starting mongodb 
https://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/#run-mongodb-community-edition
go to C:\mongodb\bin

in cmd run mongod.exe --dbpath "d:\...."

to use shell
go to C:\mongodb\bin in another cmd window
in cmd run mongo.exe
> db.test.find()

'''

client = MongoClient()
db = client.db
coll = db.test

#result = db.test.delete_many({})
# cursor = db.test.find()
# for document in cursor:
# 	print (document)

#sys.exit()

#test = parser_pbp.DataAccess('http://www.nhl.com/scores/htmlreports/20142015/PL020014.HTM')
#test.Output()

def CheckGameExists(gameId, collection):
	'''Check if the game is already loaded in a particular collection'''
	cursor = collection.find( {"game_id" : gameId})
	for document in cursor:
		print document
	if cursor.count() > 0:
		return 1
	else:
		return 0

yearString = "20142015"
gameId = 78
while (True):
	gameIdStr = format(gameId, '04')	#format with leading zeros
	
	print CheckGameExists(yearString +gameIdStr, db.eventSummary)
	print yearString + gameIdStr
	sys.exit()

	#urlString = "http://www.nhl.com/scores/htmlreports/20142015/PL020014.HTM"	
	#Parse for the PBP file and insert into db
	if CheckGameExists(yearString + gameIdStr, db.test) == 0:
		pbp_parse = parser_pbp.DataAccess(yearString, gameIdStr)
		pbp_result = pbp_parse.Output()	

		if (pbp_result):
			pbp_result = db.test.insert_one(pbp_result)

		print "PBP Parsed"

	#Parse for the event summary file and insert into db
	if CheckGameExists(yearString + gameIdStr, db.eventSummary) == 0:
		es_parse = parser_event_summary.DataAccess(yearString, gameIdStr)
		es_result = es_parse.Output()


		if (es_result):
			es_result = db.eventSummary.insert_one(es_result)

		print "ES Parsed"
	gameId = gameId + 1
	print yearString + gameIdStr
	sys.exit()


sys.exit()

'''
team document
{
	"team_name"
	"players" :[
		"----" : ID,
	]
}

player document
{
	"name" : ,
	"dob" : ,		
	"status" : ,	healthy, injured, etc
	"current" : ,	is player data updated? put most recent gameID
	"stats" :
		{
			"team_id" : ,
			"gp" : ,
			"goals" : ,
			"assists" :,
			"plusMinus" : ,

		}
}

playbyplay document
{
	"game_id" : ,
	"home_team" : ,
	"away_team" : ,
	"date" : ,
	"pbp" : [
			{
				"period" :
				"strength" :
				"time" :
				"event" :
				"event_desc" :
				"home_players" : [
					"LW"
					"C"
					"RW"
					"D"
					"D"
					"G"
				]
				"away_players" : [
					"LW"
					"C"
					"RW"
					"D"
					"D"
					"G"
				]

			}
	]

}

eventsummary document
{
	"game_id"
	"home_team"
	"away_team"
	"date"
	"homeTeamPlayers" : [
		[
					"jersey"
					"position"
					"name"
					"goals"
					"assists"
					"plus minus"
					"penalities"
					'pim'
					'tot'
					'shifts'
					'ppTime'
					'shTime'
					'evenTime'
					'shotsOnGoal'
					'shotsBlocked'
					'shotsMissed'
					'hits'
					'giveaways'
					'takeaways'
					'blocks'
					'fWins'
					'fLoss']
		...repeat for each player
		]
	"awayTeamPlayers" : [
		{
		"<PLAYER NAME>" : [
				
			....
				]
		}]
}
'''