from bs4 import BeautifulSoup
import urllib2
import sys
import re
import json
import datetime

# Parser for PLAY BY PLAY pages


class Event:
    '''Attributes: 
        - playID
        - period
        - homeTeam
        - awayTeam
        - homeTeamStatus
        - awayTeamStatus
        - timeInPeriod
        - eventType
        - desc
        - homeTeam players array
        - awayTeam palyers array
        
        '''
    def __init__(self):
        self.playId = None
        self.period = None

        self.homeTeamStatus = None
        self.awayTeamStatus = None
        self.timeInPeriod = None
        self.eventType = None
        self.desc = None

        self.homeTeam = []
        self.awayTeam = []

    def ConvertUnicodeToInteger(self, value):
        ''' Used to convert the unicode values into integers when appropriate
             First check if it is unicode
             If the unicode chracter is blank( ie ord(<unicode>) == 160), then assign integer 0
            Else, try to convert to integer'''
        if isinstance(value, unicode):
            if ord(value)==160:
                value = 0
            else:
                value = int(value)
        return value

    def ConvertUnicodeToFloat(self, value):
        '''Used to convert the unicode values into integers when appropriate
             First check if it is unicode
             If the unicode chracter is blank( ie ord(<unicode>) == 160), then assign integer 0
            Else, try to convert to integer'''
        if isinstance(value, unicode):
            if ord(value)==160:
                value = 0
            else:
                value = float(value)
        return value

class GoalEvent(Event):
    '''Example String Desc MIN #29 POMINVILLE(1), Wrist, Off. Zone, 16 ft.
            Assists: #64 GRANLUND(1); #20 SUTER(1)'''
    #Inherits Event instance values into this GoalEvent instance
    #https://mygisblog.wordpress.com/2010/06/29/instance-inheritance-python-my-project-contd/
    _inherited = ['playId']
    def __init__(self):
        self._parent = event

    def __getattr__(self, name):
        if name in self._inherited:
            return getattr(self._parent,name)
        return self.__dict__[name]
    
class DataAccess:
    '''Composition of Parser object with events, used for serializing into JSON for MongoDB'''
    def __init__(self, url):
        self.parser = Parser(url)
        self.parser.GameInfoParse()
        self.parser.VisitingTeamInfoParse()
        self.parser.HomeTeamInfoParse()
        self.parser.EventSummaryParse()

    def Output(self):
        '''Make output to '''
        self.game_id = 0
        self.home_team = self.parser.homeTeam
        self.away_team = self.parser.visitingTeam

        self.date = self.parser.date
        self.pbp = []
        for event in self.parser.eventSeries:
            #self.pbp.append(json.dumps(event.__dict__))
            #-----
            self.pbp.append({'playId' : event.playId,
                            'period' : event.period,
                            'homeTeamStatus' : event.homeTeamStatus,
                            'awayTeamStatus' : event.awayTeamStatus,
                            'timeInPeriod' : event.timeInPeriod,
                            'eventType' : event.eventType,
                            'desc' : event.desc,
                            'homeTeam' : event.homeTeam,
                            'awayTeam' : event.awayTeam 
                            })
            
        #Delete the parser object so object is not seriazlied
        self.parser = None
        del self.parser

        self.jsonOutput = json.dumps(self.__dict__)
        return self.jsonOutput

    def Prettify(self):
        del self.jsonOutput
        self.jsonOutput = json.dumps(self.__dict__, sort_keys=True, indent=4, separators=(',', ': '))
        return self.jsonOutput



class Parser:
    '''Parses Game Info, Visiting Team, Home Team, and Play by Play'''
    def __init__(self, url):
        self.url = url
        self.page = urllib2.urlopen(self.url)
        self.soup = BeautifulSoup(self.page.read(), "html.parser")
        self.body = self.soup.find("table")

        self.eventSeries = []

    def GameInfoParse(self):
        '''Grab info such as date, attendance'''
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

        # self.attendance stores the attendance info as Attendance 19,745 at Air Canada Centre
        self.attendanceNode = self.gameInfoNode.find("td")
        self.attendance = self.attendanceNode.string

        return True

    def VisitingTeamInfoParse(self):
        '''Grabs the visiting team info
        - Team Name'''
        # Start at the node for the visiting team
        #< table id="Visitor" border="0" cellpadding="0" cellspacing="0" align="center">
            # <tbody><tr>
            #     <td align="center" style="font-size: 12px;font-weight:bold">VISITOR</td>
            # </tr>
            # <tr>
            # <td>
            # <table border="0" cellpadding="4" cellspacing="20" align="center">
            # <tbody><tr>
            #     <td align="center"><img src="http://www.nhl.com/scores/htmlreports/images/logoccol.gif" alt="COLORADO AVALANCHE" width="50" height="50" border="0"></td>
            #     <td align="center" style="font-size: 40px;font-weight:bold">0</td>
            #     <td align="center"><img src="http://www.nhl.com/scores/htmlreports/images/logocnhl.gif" width="50" height="50" border="0"></td>
            # </tr>
            # </tbody></table>
            # </td>
            # </tr>
            # <tr>
            #     <td align="center" style="font-size: 10px;font-weight:bold">COLORADO AVALANCHE<br>Game 1 Away Game 1</td>
            # </tr>
        # </tbody></table>
        self.visitingTeamNode = self.body.find("table", {"id": "Visitor"})
        self.visitingTeamNode = self.visitingTeamNode.find("td", {"style" : "font-size: 10px;font-weight:bold"})

        #<td align="center" style="font-size: 10px;font-weight:bold">COLORADO AVALANCHE<br>Game 1 Away Game 1</td>
        #if we find_all texts, then we get a list [COLORADO, GAME 1 AWAY GAME 1]
        self.visitingTeam = self.visitingTeamNode.find_all(text = True)[0]

    def HomeTeamInfoParse(self):
        '''Grabs the home team info
        - Team Name'''
        # See above for visiting team
        self.homeTeamNode = self.body.find("table", {"id": "Home"})
        self.homeTeamNode = self.homeTeamNode.find("td", {"style" : "font-size: 10px;font-weight:bold"})

        #<td align="center" style="font-size: 10px;font-weight:bold">COLORADO AVALANCHE<br>Game 1 Away Game 1</td>
        #if we find_all texts, then we get a list [COLORADO, GAME 1 AWAY GAME 1]
        self.homeTeam = self.homeTeamNode.find_all(text = True)[0]

    def EventSummaryParse(self):
        '''Go through the play by play'''

        self.periodTable = self.body
        #Table Tag for beginning of period: 
        #<table align="center" border="0" cellpadding="0" cellspacing="0" class= "tablewidth">
        while (self.periodTable):
            # Start at first <tr class="evenColor"> and loop
            self.eventRow = self.periodTable.find("tr", {"class" : "evenColor"})

            while (self.eventRow):      #loops until all are found

                self.eventSeries.append(Event())
                self.ParseRow()
                #move to the next row
                self.eventRow = self.eventRow.findNextSibling("tr", {"class" : "evenColor"})

            #move to the next table (new period)
            self.periodTable = self.periodTable.findNextSibling("table", {"align" : "center", "border" : "0", "cellpadding" : "0", "cellspacing" : "0", "class" : "tablewidth"})
 

    def ParseRow(self):
        #Parse play ID
        currentEvent = len(self.eventSeries) - 1
        self.eventRowNode = self.eventRow.find("td")
        self.eventSeries[currentEvent].playId = self.eventRowNode.string
        
        #Period 
        self.eventRowNode = self.eventRowNode.nextSibling.nextSibling
        self.eventSeries[currentEvent].period = self.eventRowNode.string

        #Strength
        self.eventRowNode = self.eventRowNode.nextSibling.nextSibling
        self.eventSeries[currentEvent].homeTeamStatus = self.eventRowNode.string
  
                
        #Time        
        self.eventRowNode = self.eventRowNode.nextSibling.nextSibling      
        self.eventRowNodeNode = self.eventRowNode.findAll()
        for strings in self.eventRowNode.strings:
            self.eventSeries[currentEvent].timeInPeriod = repr(strings)
            break

        #Event type
        self.eventRowNode = self.eventRowNode.nextSibling.nextSibling
        self.eventSeries[currentEvent].eventType = self.eventRowNode.string
        if (self.eventRowNode.string == "GEND"):
            #quit since it is end of game
            return

        #Event description
        self.eventRowNode = self.eventRowNode.nextSibling.nextSibling
        self.eventSeries[currentEvent].desc = self.eventRowNode.string

        #Away Team
        playerTable = self.eventRow.find("table", attrs={'border':'0', 'cellpadding' : '0', 'cellspacing' : '0'})
        players = playerTable.findAll("font")
        for player in players:
            self.eventSeries[currentEvent].homeTeam.append(player['title'])
            
        #Home Team
        playerTable = self.eventRow.find_all("td", attrs={'class' : ' + bborder'})      
        if len(playerTable) == 0:
            #the following td class tag occurs occasionally (when there is penalty)
            playerTable = self.eventRow.find_all("td", attrs={'class' : 'italicize + bold + bborder'})
        if len(playerTable) == 0:
            #the following td class tag occurs occasionally (when there is goal)
            playerTable = self.eventRow.find_all("td", attrs={'class' : 'bold + bborder'})

        #grab the LAST td class + bborder to get this table of players
        playerTable = playerTable[-1]

        players = playerTable.find_all("font")
        for player in players:
            self.eventSeries[currentEvent].awayTeam.append(player['title'])
            

    
def main():

    newParse = Parser("http://www.nhl.com/scores/htmlreports/20142015/PL020014.HTM")
    newParse.GameInfoParse()
    newParse.VisitingTeamInfoParse()
    newParse.HomeTeamInfoParse()
    print newParse.visitingTeam
    print newParse.homeTeam
    print newParse.date
    newParse.EventSummaryParse()
    

if __name__ == "__main__":
    main()