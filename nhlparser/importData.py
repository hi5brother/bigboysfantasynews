from pymongo import MongoClient
import json
import parser_pbp
import parser_event_summary
import sys

client = MongoClient()
db = client.db
coll = db.test

# result = db.test.insert_one(
# 	{

# 		"player" : "Jason Spezza",
# 		"number" : 19
# 	})



#test = parser_pbp.DataAccess('http://www.nhl.com/scores/htmlreports/20142015/PL020014.HTM')
#test.Output()

test = parser_event_summary.DataAccess('http://www.nhl.com/scores/htmlreports/20142015/ES020014.HTM')
test.Output()

with open('test.txt', 'w') as txtfile:
	txtfile.write(test.Prettify())


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