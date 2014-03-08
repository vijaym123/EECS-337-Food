import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json
import re
import difflib
import nltk
import fractions
from collections import defaultdict
import wikipedia


recipesData = []

def labelIngredients(ingredientText, amountText):
	"""
	amount = number + measurement
	ingredient = descriptor + preparation + item
	"""
	tokens = nltk.word_tokenize(ingredientText.replace(",",""))
	tags = nltk.pos_tag(tokens)
	label = defaultdict(list)
	label["ingredient"] = ingredientText
	for i in tags:
		if i[1].startswith("JJ"):
			label["descriptor"].append(i[0])
		elif i[1].startswith("RB") or i[1].startswith("VB"):
			label["preparation"].append(i[0])
		else:
			label["item"].append(i[0])

	label["descriptor"] = " ".join(label["descriptor"])
	label["preparation"] = " ".join(label["preparation"])
	label["item"] = " ".join(label["item"])
	
	tokens = nltk.word_tokenize(amountText.replace(",",""))
	label["amount"] = amountText
	label["number"] = 0
	label["measurement"] = []
	for i in tokens:
		try:
			label["number"] +=  float(fractions.Fraction(i))
		except ValueError:
			label["measurement"].append(i)
	label["measurement"] = " ".join(label["measurement"])
	return dict(label) 

def getIngredients(soupBody):
	iterator = zip([i.text for i in soupBody.findAll("span",{"id":"lblIngName"})],[ i.text for i in soupBody.findAll("span",{"id":"lblIngAmount"})])
	return [labelIngredients(item[0],item[1]) for item in iterator]

def main():
	number = 1
	page = url.urlopen("http://allrecipes.com/recipes/breakfast-and-brunch/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
	recipeNames = []
	while page:
		soupBody = BeautifulSoup(page)
		recipeNames.extend([ (i.find('a').text, i.find('a')["href"]) for i in soupBody.findAll('h3',{"class":"resultTitle"})])
		number = number + 1
		page = url.urlopen("http://allrecipes.com/recipes/breakfast-and-brunch/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
		if number == 20:
			break
	return dict(recipeNames)