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

yearString = "20142015"
gameId = 0004
while (True):
	gameIdStr = format(gameId, '04')

	#urlString = "http://www.nhl.com/scores/htmlreports/20142015/PL020014.HTM"
	test = parser_pbp.DataAccess(yearString, gameIdStr)
	result = test.Output()
	print yearString + gameIdStr
	#print urlString

	if (True):
		 with open('test_pbp.txt', 'w') as txtfile:
		 	#txtfile.write(json.dumps(test.Prettify()))
		 	txtfile.write(json.dumps(result))

			result = db.test.insert_one(result)
			gameId = gameId + 1	

	else:
		break

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
	"status" : ,
	"current_team" :
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