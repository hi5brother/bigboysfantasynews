from requests_oauthlib import OAuth1Session
import requests
import webbrowser
#--------------------------------------
#Big Boys Fantasy News
#Dec 29, 2014
#Daniel Kao
#OAuth1 Authenticaion to get access token ---> Yahoo Fantasy Sports API calls
#--------------------------------------

CONSUMER_KEY = 'dj0yJmk9TEw1d1Z1cjZBc2twJmQ9WVdrOVRuSm9SVTVHTjJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hNA--'
CONSUMER_SECRET = '33a3bd1538130fce758ccbed6be86bb82bbd5f14'

REQUEST_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
ACCESS_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'

LEAGUE_KEY = "341.l.9496"


class YahooHandler():

	def __init__(self):
		pass

	def get_request_token(self):
		#Request Token from Yahoo
		oauth = OAuth1Session(CONSUMER_KEY, 
								client_secret=CONSUMER_SECRET, 
								callback_uri="oob")

		fetch_response = oauth.fetch_request_token(REQUEST_URL)

		self.resource_owner_key = fetch_response.get('oauth_token')
		self.resource_owner_secret = fetch_response.get('oauth_token_secret')

		authorization = oauth.authorization_url(AUTHORIZATION_URL)
		authorization_oauth_token = authorization[authorization.index("=") + 1:]	#finds the part of the authorization URL that is the request token (code after ?oauth_token=..._)
		webbrowser.open_new_tab(authorization)

		print "The oauth token is " + authorization_oauth_token

		self.verifier = raw_input("Input the verifier.\n")

		return True

	def get_access_token(self):
		#Get access token from the request and verifier
		oauth = OAuth1Session(CONSUMER_KEY, 
						client_secret=CONSUMER_SECRET, 
						resource_owner_key=self.resource_owner_key, 
						resource_owner_secret=self.resource_owner_secret, 
						verifier=self.verifier)
		oauth_tokens = oauth.fetch_access_token(ACCESS_URL)

		self.access_token_key = oauth_tokens.get('oauth_token')
		self.access_token_secret = oauth_tokens.get('oauth_token_secret')

		return True

	def refresh_access_token(self):
		#Refresh the access token after 1 hour
		#oauth1session library might not support this...
		oauth = OAuth1Session(CONSUMER_KEY, 
				client_secret=CONSUMER_SECRET, 
				resource_owner_key=self.resource_owner_key, 
				resource_owner_secret=self.resource_owner_secret,
				oauth_token=self.access_token_key,
				verifier=self.verifier)
		oauth_tokens = oauth.fetch_access_token(ACCESS_URL)

		self.access_token_key = oauth_tokens.get('oauth_token')
		self.access_token_secret = oauth_tokens.get('oauth_token_secret')

		return True

	def process_tokens(self):
		#use this method to create all the access tokens
		self.get_request_token()
		self.get_access_token()

	def api_call(self,request_string):
		#We will use requests to the API that are determined by the request_string
		req_oauth = OAuth1Session(CONSUMER_KEY,
									client_secret=CONSUMER_SECRET,
									resource_owner_key=self.access_token_key,
									resource_owner_secret=self.access_token_secret)

		#league key is 341.l.9496
		r = req_oauth.get('http://fantasysports.yahooapis.com/fantasy/v2/league/341.l.9496/' + request_string)
		
		#print r.text

		return r.text

class YQlHandler(YahooHandler):
	def __init__(self):
		self.process_tokens()

	def get_query_params(self, query, params, **kwargs):
		query_params={}
		if query.validation(params) and parmas:
			query_params.update(params)
		query_params['q'] = query.query
		query_params['format'] = 'json'

		env = kwargs.get('env')
		if env:
			query_params['env'] = env

		return query_params


	def get_uri(self, query, params=None, **kwargs):
		"""Get the the request url"""
		if isinstance(query, basestring):
			query = YQLQuery(query)
		params = self.get_query_params(query, params, **kwargs)
		query_string = urlencode(params)
		uri = '%s?%s' % (self.endpoint, query_string)
		uri = clean_url(uri)
		return uri

	def execute(self, query, params=None, **kwargs):
		"""Execute YQL query"""
		yqlquery = YQLQuery(query)
		url = self.get_uri(yqlquery, params, **kwargs)
		yql_logger.debug("executed url: %s", url)
		http_method = yqlquery.get_http_method()
		if http_method in ["DELETE", "PUT", "POST"]:
			data = {"q": query}
			# Encode as json and set Content-Type header
			# to reflect we are sending JSON
			# Fixes LP: 629064
			data = json.dumps(data)
			headers = {"Content-Type": "application/json"}
			resp, content = self.http.request(
							url, http_method, headers=headers, body=data)
			yql_logger.debug("body: %s", data)
		else:
			resp, content = self.http.request(url, http_method)

		yql_logger.debug("http_method: %s", http_method)
		if resp.get('status') == '200':
			return YQLObj(json.loads(content))
		else:
			raise YQLError(resp, content)


def main():
	#Main program loop, will ask for requests and output the data in a lopp
	
	instance = YahooHandler()
	instance.process_tokens()
	
	"""while True:
		request = raw_input("Please type your request: (try standings, scoreboard) \n")
		instance.api_call(request)
	"""
