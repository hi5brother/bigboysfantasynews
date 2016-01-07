import xml.etree.ElementTree as ET
import request_api

import xml_parser

#---------------------------------------
#Big Boys Fantasy News
#Dec 30, 2014
#Daniel Kao
#Parse xml data from Yahoo Fantasy API using python xml.etree
#---------------------------------------

LEAGUE_KEY = "341.l.9496"
CONSUMER_KEY = 'dj0yJmk9TEw1d1Z1cjZBc2twJmQ9WVdrOVRuSm9SVTVHTjJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hNA--'
BASE_URL = "{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}"

def main():
	instance = request_api.YahooHandler()
	instance.process_tokens()
	
	xml = instance.api_call("teams")
	data = ET.fromstring(xml)

	print xml_parser.parse(data,"name")
	print xml_parser.parse(data,"team_key")
	print xml_parser.parse(data,"team_id")

	#root = data.getroot()

	#print root.tag, root.attrib

	# for team in data.getiterator():
	#  	if team.tag:
	#  		print team.tag[team.tag.index("}")+1:]	
	#  	if team.text:
	# 		#print 'my text:'+'\t'+(team.text).strip()
	# 		pass
	# 	if team.attrib.items():
	# 		print 'my attributes:'
	# 		for key, value in team.attrib.items():
	# 			print "KEY: " +key + ' : ' + value



	# for team in data.iter(tag=BASE_URL+'full'):
	# 	print team.text
	# for elem in data.iter(tag=BASE_URL+'player_key'):
	# 	print elem.text
		#print team.text

	# for team in data.iter():
	# 	if team.tag is BASE_URL+'name':
	# 		print team.text
	# print BASE_URL+'name'

	#instance = request_api.YQLHandler()

main()