import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json
import nltk
from collections import defaultdict
import re
import difflib

def getItems(ingredientText):
	"""
	ingredient = descriptor + preparation + item
	"""
	global ingredientsBook

	ingredientText=ingredientText.replace(",","")
	tokens = nltk.word_tokenize(ingredientText)
	tags = nltk.pos_tag(tokens)
	label = defaultdict(list)
	label["ingredient"] = ingredientText

	if difflib.get_close_matches(ingredientText, ingredientsBook):
		label["item"].append(ingredientText)
	else:
		for i in tags:
			if i[1].startswith("JJ"):
				label["descriptor"].append(i[0])
			elif i[1].startswith("RB") or i[1].startswith("VB"):
				label["preparation"].append(i[0])
			else :
				label["item"].append(i[0])

	label["descriptor"] = " ".join(label["descriptor"])
	label["preparation"] = " ".join(label["preparation"])
	label["item"] = " ".join(label["item"])
	# if label["item"] == '':
	# 	print label['descriptor'],"----",label['preparation'],"----",label['ingredient'] 
	return label["item"]

def getIngredients(link):
	page = url.urlopen(str(link))
	soupBody = BeautifulSoup(page)
	items = [ getItems(i.text) for i in soupBody.findAll("span",{"id":"lblIngName"})]
	while items.count('')!=0:
		items.remove('')
	return items

def getAllIngredients():
	title = "http://en.wikibooks.org/wiki/"
	page = url.urlopen(title+"Cookbook:Ingredients")
	if page:
		soupBody = BeautifulSoup(page)
		ingredients = dict([(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})[1:-5]])
	return ingredients.keys()

if __name__ == "__main__":
	number = 1
	maxNumber = 30
	page = url.urlopen("http://allrecipes.com/recipes/breakfast-and-brunch/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
	recipeNames = []
	
	global ingredientsBook
	ingredientsBook = getAllIngredients()

	while page:
		print number
		soupBody = BeautifulSoup(page)
		recipeNames.extend([ (i.find('a').text, { "url" : i.find('a')["href"], "recipe" : getIngredients(i.find('a')["href"]) }) for i in soupBody.findAll('h3',{"class":"resultTitle"})])
		number = number + 1
		page = url.urlopen("http://allrecipes.com/recipes/breakfast-and-brunch/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
		if number >= maxNumber:
			break
	data = dict(recipeNames)
	print data
	filename = "breakfast-and-brunch.data"
	f = open(filename,"w")
	f.write(json.dumps(data))
	f.close()