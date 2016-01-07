<h1>Big Boys Fantasy News</h1>
<h2>Project Information</h2>
<h3>Objectives</h3>
<ol>
	<li>Access Yahoo Fantasy Hockey data using Yahoo Fantasy API </li>
	<li>Provide up to date information of fantasy teams from Yahoo's fantasy leagues</li>
	<li>Scrape statistics data off of NHL.com and generate analytics in-house</li>
</ol>

<h3>Project Deliverables</h3>
<ol>
	<li>Access Yahoo fantasy data specific to user</li>
	<li>Desktop scripts to parse NHL.com data into local database </li>
	<li>Excel add-in to link Excel Spreadsheet frontend to local database
	<li>Documentation for using program</li>
</ol>
<h2>Program Use and Information<h3>
<h3>Current Version</h3>
Version 0.2
<h3>Change Log</h3>
Version 0.2
<ul>
	<li>Parses Event Summary pages from NHL.com</li>
</ul>
Version 0.1
<ul>
	<li>Can query standard requests about league information (e.g.standings, scoreboard, players)</li>
	<li>Only outputs data in xml in command prompt</li>

</ul>
<h3>Known Issues</h3>
<ul>

	<li>The Requests-OAuthLib does not support refreshing of access token for OAuth1</li>

</ul>
<h3>Modules Used</h3>
<ul>
	<li><a href="https://pypi.python.org/pypi/beautifulsoup4">Beautiful Soup 4</li>
	<li><a href="https://github.com/requests/requests-oauthlib">Requests-OAuthLib</a></li>
	<li><a href="https://github.com/kennethreitz/requests">Requests</a></li>

</ul>
<h2>Potential Future Plans and Applications</h2>
<ul>
	<li>Put the backend into a LAMP stack</li>
	<li>Add RSS feed about the teams</li>
</ul>