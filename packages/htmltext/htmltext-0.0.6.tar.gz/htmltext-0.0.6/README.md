#HTMLText
=========
htmltext is a simple tool to get main body text of articles in HTML web pages, such as news,bolg .etc.

Installation:
-------------
	pip install htmltext

Usage:
------
	from htmltext import HTMLText
	
	title, text = HTMLText(html_data)

Example:
--------
	import requests
	from htmltext import HTMLText
	
	r = requests.get(url_of_the_article)
	title, text = HTMLText(r.content)
	print(title)
	print(text)


