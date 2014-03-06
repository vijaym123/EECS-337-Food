import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json

def getTable():
	page = url.urlopen("http://allrecipes.com/howto/common-ingredient-substitutions/")
	soup = BeautifulSoup(page)
	table = soup.find("table")
	subs = []
	index = 0
	for row in table.find_all('tr'):
		col = row.findAll('td')
		subs.append([])
		for co in col:
			splitco = co.findAll('strong')
			for spl in splitco:
				subs[index].append(spl.text.encode('ascii','ignore'))
		index = index + 1
	print subs
	return subs

if __name__ == "__main__":
	getTable()