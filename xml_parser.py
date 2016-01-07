import xml.etree.ElementTree as ET


LEAGUE_KEY = "341.l.9496"
CONSUMER_KEY = 'dj0yJmk9TEw1d1Z1cjZBc2twJmQ9WVdrOVRuSm9SVTVHTjJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hNA--'
BASE_URL = "{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}"

def parse(data, field):
	#data = ET.fromstring(raw_data)

	return_data = []

	for elem in data.getiterator(tag=BASE_URL+field):
		if elem.tag:
			return_data.append(elem.text)

	return return_data
	#when return teams

