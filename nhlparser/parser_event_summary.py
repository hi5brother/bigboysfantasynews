from bs4 import BeautifulSoup
import urllib2
import sys
import json
import datetime

# Parser for EVENT SUMMARY pages

class Player:
	'''Class that stores stats of each player in the Event Summary'''
	def __init__(self):
		self.team = None

		self.jersey = None			# 0th column
		self.position = None		# 1st column
		self.name = None			
		self.goals = None
		self.assists = None
		self.points = None			# 5th column
		self.plusMinus = None
		self.penalties = None
		self.pim = None
		self.tot = None
		self.shifts = None			# 10th column
		self.ppTime = None			# We skipped average time per shift (11th column)
		self.shTime = None
		self.evenTime = None
		self.shotsOnGoal = None		# 15th column
		self.shotsBlocked = None
		self.shotsMissed = None
		self.hits = None
		self.giveaways = None
		self.takeaways = None		# 20th column
		self.blocks = None
		self.fWins = None
		self.fLoss = None			# 23rd column (we skipped the 24th column, faceoff %)

	def ValidateData(self):
		self.goals = self.ConvertUnicodeToInteger(self.goals)
		self.assists = self.ConvertUnicodeToInteger(self.assists)
		self.points = self.ConvertUnicodeToInteger(self.points)
		
		# Need to convert with the +/- signs
		if ord(self.plusMinus[0])==160:
			self.plusMinus = 0
		elif self.plusMinus[:1] == "+":
			self.plusMinus = self.ConvertUnicodeToInteger(self.plusMinus[1:])
			self.plusMinus = self.plusMinus * 1
		elif self.plusMinus[:1] == "-":
			self.plusMinus = self.ConvertUnicodeToInteger(self.plusMinus[1:])
			self.plusMinus = self.plusMinus * (-1)

		self.penalties = self.ConvertUnicodeToInteger(self.penalties)
		self.pim = self.ConvertUnicodeToInteger(self.pim)

		self.shifts = self.ConvertUnicodeToInteger(self.shifts)

		self.shotsOnGoal = self.ConvertUnicodeToInteger(self.shotsOnGoal)
		self.shotsBlocked = self.ConvertUnicodeToInteger(self.shotsBlocked)
		self.shotsMissed = self.ConvertUnicodeToInteger(self.shotsMissed)
		self.hits = self.ConvertUnicodeToInteger(self.hits)
		self.giveaways = self.ConvertUnicodeToInteger(self.giveaways)
		self.takeaways = self.ConvertUnicodeToInteger(self.takeaways)
		self.blocks = self.ConvertUnicodeToInteger(self.blocks)
		self.fWins = self.ConvertUnicodeToInteger(self.fWins)
		self.fLoss = self.ConvertUnicodeToInteger(self.fLoss)

	
	def ConvertUnicodeToInteger(self, value):
		'''Used to convert the unicode values into integers when appropriate'''
		# 	First check if it is unicode
		# 	If the unicode chracter is blank( ie ord(<unicode>) == 160), then assign integer 0
		#	Else, try to convert to integer
		sumTot = 0
		place = len(value)

		if isinstance(value, unicode):
			if len(value)== 1:
				if ord(value)==160:
					value = 0
				else:
					value = int(value)
			elif len(value) > 1:
				for val in value:
					sumTot += int(value) * (10^place)
					place -= 1

			return value

	def ConvertUnicodeToFloat(self, value):
		# Used to convert the unicode values into integers when appropriate
		# 	First check if it is unicode
		# 	If the unicode chracter is blank( ie ord(<unicode>) == 160), then assign integer 0
		#	Else, try to convert to integer
		if isinstance(value, unicode):
			if ord(value)==160:
				value = 0
			else:
				value = float(value)
		return value

class DataAccess:
	'''Composition of Parser object for event summary, used to serialize JSON output to MongoDB'''
	def __init__(self, url):
		self.parser = Parser(url)

		self.parser.HomeTeamParse()
		self.parser.VisitingTeamParse()
		self.parser.GameInfoParse()

	def Output(self):
		'''Make Output to '''
		if (self.parser.errorStatus):
			return False

		self.home_team = self.parser.homeTeam
		self.away_team = self.parser.visitingTeam
		self.date = self.parser.date
		self.homePlayers = []
		self.awayPlayers = []
		for player in self.parser.homePlayers:
			self.homePlayers.append({
				'jersey' : player.jersey,
				'position' : player.position,
				'name' : player.name,
				'goals' : player.goals,
				'assists' : player.assists,
				'plusMinus' : player.plusMinus,
				'penalties' : player.penalties,
				'pim' : player.pim,
				'tot' : player.tot,
				'shifts' : player.shifts,
				'ppTime' : player.ppTime,
				'shTime' : player.shTime,
				'evenTime' : player.evenTime,
				'shotsOnGoal' : player.shotsOnGoal,
				'shotsBlocked' : player.shotsBlocked,
				'shotsMissed' : player.shotsMissed,
				'hits' : player.hits,
				'giveaways' : player.giveaways,
				'takeaways' : player.takeaways,
				'blocks' : player.blocks,
				'fWins' : player.fWins,
				'fLoss' : player.fLoss
				})

		for player in self.parser.visitingPlayers:
			self.awayPlayers.append({
				'jersey' : player.jersey,
				'position' : player.position,
				'name' : player.name,
				'goals' : player.goals,
				'assists' : player.assists,
				'plusMinus' : player.plusMinus,
				'penalties' : player.penalties,
				'pim' : player.pim,
				'tot' : player.tot,
				'shifts' : player.shifts,
				'ppTime' : player.ppTime,
				'shTime' : player.shTime,
				'evenTime' : player.evenTime,
				'shotsOnGoal' : player.shotsOnGoal,
				'shotsBlocked' : player.shotsBlocked,
				'shotsMissed' : player.shotsMissed,
				'hits' : player.hits,
				'giveaways' : player.giveaways,
				'takeaways' : player.takeaways,
				'blocks' : player.blocks,
				'fWins' : player.fWins,
				'fLoss' : player.fLoss
				})

		self.parser = None
		del self.parser
		#self.jsonOutput = json.dumps(self.__dict__)
		#return self.jsonOutput

	def Prettify(self):

		del self.jsonOutput
		self.jsonOutput = json.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ': '))
		return self.jsonOutput




class Parser:
	'''Parses Game Info, visiting Team and Home Team players and their stats'''
	def __init__(self, url):
		try:
			self.page = urllib2.urlopen(url)
			self.soup = BeautifulSoup(self.page.read(), "html.parser")
			self.body = self.soup.find("table")
			self.errorStatus = False
		except urllib2.HTTPError:
			self.errorStatus = True


	def GameInfoParse(self):
		'''Grab game info, such as date and attendance'''
		
		if (self.errorStatus):
			return False

		# Find the node with GameInfo
		self.gameInfo = self.body.find("table", {"id" : "GameInfo"})
		self.gameInfoNode = self.gameInfo.find("tr")

		# Look through a couple of rows until the date information is known
		self.gameInfoNode = self.gameInfoNode.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling

		# self.date contains the date as Wednesday, October 8, 2015 (unicode)
		self.dateNode = self.gameInfoNode.find("td")
		self.date = self.dateNode.string

		#Use datetime to convert unicode date to string as month/day/year 08/10/2015
		self.date = datetime.datetime.strptime(self.date, '%A, %B %d, %Y').strftime('%m/%d/%Y')

		self.gameInfoNode = self.gameInfoNode.nextSibling.nextSibling

		# self.attendance returns the attendance info as Attendance 19,745 at Air Canada Centre
		self.attendanceNode = self.gameInfoNode.find("td")
		self.attendance = self.attendanceNode.string

		return True

	def VisitingTeamParse(self):
		'''Go through player stats on the visiting team'''

		if (self.errorStatus):
			return False

		# Start at the node for the visiting team
		self.visitingTeamNode = self.body.find("td", {"class" : "lborder + rborder + bborder + visitorsectionheading"})
		self.visitingTeam = self.visitingTeamNode.string 	#returns the name of the visiting team

		# Go up one node and start looping through players
		self.playerRowNode = self.visitingTeamNode.parent

		self.playerNode = self.playerRowNode.nextSibling.nextSibling.nextSibling.nextSibling
		
		self.visitingPlayers = []

		# Find all the player rows 
		while (self.playerNode["class"][0]==("evenColor") or self.playerNode["class"][0]==("oddColor"))and self.playerNode["class"][0]!="oddColor + bold" and self.playerNode["class"][0]!="evenColor + bold":

			# Parse the node for all attributes of a player
			player = self.ReturnPlayer(self.visitingTeam)
			if (player):
				self.visitingPlayers.append(player)
			
			# Iterate to the next player node
			self.playerNode = self.playerNode.nextSibling.nextSibling

			try:		# If calling for an attribute fails, we will quit the loop
				self.playerNode["class"]
			except Exception:
				break

		return True

	def HomeTeamParse(self):
		'''Go through player stats on the home team'''

		if (self.errorStatus):
			return False

		# Start at the node for the home team
		self.homeTeamNode = self.body.find("td", {"class" : "lborder + rborder + bborder + homesectionheading"})
		self.homeTeam = self.homeTeamNode.string 	#returns the name of the hometeam

		# Go up one node and start looping through players
		self.playerRowNode = self.homeTeamNode.parent

		# Go down a couple of nodes past the header tr nodes
		self.playerNode = self.playerRowNode.nextSibling.nextSibling.nextSibling.nextSibling
		
		self.homePlayers = []

		# Find all the player rows 
		while (self.playerNode["class"][0]==("evenColor") or self.playerNode["class"][0]==("oddColor")) and self.playerNode["class"][0]!="oddColor + bold" and self.playerNode["class"][0]!="evenColor + bold":

			# Parse the node for all attributes of a player
			player = self.ReturnPlayer(self.homeTeam)
			if (player):
				self.homePlayers.append(player)
			
			# Iterate to the next player node
			self.playerNode = self.playerNode.nextSibling.nextSibling

			try:		# If calling for an attribute fails, we will quit the loop
				self.playerNode["class"]
			except Exception:
				break

		return True

	def ReturnPlayer(self, team):
		''' Create the  player object to return, that stores all the stats'''
		
		playerValues = Player()

		playerValues.team = team

		# Grab all the child nodes of the player node that contain the stats info
		playerStats = self.playerNode.find_all("td")

		# Break if we have an invalid row
		if len(playerStats)!= 25:
			return False
		#print playerStats
		# Assign the stat nodes to the player properties
		playerValues.jersey = playerStats[0].string
		playerValues.position = playerStats[1].string
		playerValues.name = playerStats[2].string
		playerValues.goals = playerStats[3].string
		playerValues.assists = playerStats[4].string
		playerValues.points = playerStats[5].string
		playerValues.plusMinus = playerStats[6].string
		playerValues.penalties = playerStats[7].string
		playerValues.pim = playerStats[8].string
		playerValues.tot = playerStats[9].string
		playerValues.shifts = playerStats[10].string
		playerValues.ppTime = playerStats[12].string
		playerValues.shTime = playerStats[13].string
		playerValues.evenTime = playerStats[14].string
		playerValues.shotsOnGoal = playerStats[15].string
		playerValues.shotsBlocked = playerStats[16].string
		playerValues.shotsMissed = playerStats[17].string
		playerValues.hits = playerStats[18].string
		playerValues.giveaways = playerStats[19].string
		playerValues.takeaways = playerStats[20].string
		playerValues.blocks= playerStats[21].string
		playerValues.fWins = playerStats[22].string
		playerValues.fLoss = playerStats[23].string

		playerValues.ValidateData()

		return playerValues


def main():
	newParse = Parser('http://www.nhl.com/scores/htmlreports/20142015/ES201014.HTM')

	if not (newParse.errorStatus):
		newParse.HomeTeamParse()
		newParse.VisitingTeamParse()
		for player in newParse.homePlayers:


			print unicode(player.name) + unicode(" G : " + str(player.goals))
			print (player.tot)
			print (player.plusMinus)
			print (player.shotsOnGoal)

		newParse.GameInfoParse()
		print len(newParse.homePlayers)
	

if __name__ == "__main__":
    main()
    