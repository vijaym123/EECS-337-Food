import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json
import re

def getNutrients(soupBody):
	nutrients = {}
	for element in zip([i.find("li",{"class":"categories"}).text for i in soupBody.findAll("ul",{"id":"ulNutrient"})],\
						   [i.find("li",{"class":"units"})for i in soupBody.findAll("ul",{"id":"ulNutrient"})]):
		nutrients[element[0]] = (element[1].span.text, element[1].text[len(element[1].span.text):])
	return nutrients

def getIngredients(soupBody):
	return dict(zip([i.text for i in soupBody.findAll("span",{"id":"lblIngName"})],[ i.text for i in soupBody.findAll("span",{"id":"lblIngAmount"})]))

def meatAndPoultry(name):
	"""
	Source wikipedia : http://en.wikibooks.org/wiki/Cookbook:Meat_and_poultry
	"""
	meatItems = ["Beef","Bison","Dog","Game","Bear","Venison","Wild Boar","Goat",\
				"Horse","Lamb","Mutton","Pork","Rabbit","Turtle","Veal","Chicken", \
				"Cornish Game Hen","Duck","Quail","Turkey","Ostrich","Goose","Bacon",\
				"Salt Beef","Cold cuts","Ham","Sausage", "Alligator","Bison","Frog",\
				"Kangaroo","Lizard","Snake","Insects","Locust","Cricket","Honey Ant",\
				"Grubs","Whale"]
	return name in meatItems

def getAllIngredient():
	title = "http://en.wikibooks.org/wiki/"
	page = url.urlopen(title+"Cookbook:Ingredients")
	ingredients = {}
	if page:
		soupBody = BeautifulSoup(page)
		ingredients = dict([(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})[1:-5]])
	return ingredients

def getAllTechniques():
	title = "http://en.wikibooks.org/wiki/"
	page = url.urlopen(title+"Cookbook:Cooking_techniques")
	if page:
		soupBody = BeautifulSoup(page)
		techniques = dict([ (a.text,a["href"]) for ul in soupBody.findAll("ul")[2:13] for a in ul.findAll("a")])
	return techniques

def getAllEquipments():
	title = "http://en.wikibooks.org/wiki/"
	page = url.urlopen(title+"Category:Equipment")
	equipments = {}
	if page:
		soupBody = BeautifulSoup(page)
		test = [(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})]
		equipments["volume"] = test[:11]
		equipments["weight"] = test[11:17]
		equipments["length"] = test[17:21]
	return equipments

def getAllMeasurements():
	title = "http://en.wikibooks.org/wiki/"
	page = url.urlopen(title+"Cookbook:Units_of_measurement")
	if page:
		soupBody = BeautifulSoup(page)
		measurements = dict([])

def TypeOfPreparation(name):
	types = ["Baked","Baking", "Barbecue","Braise", "Camping", "Fermented", "Fried", \
			"Marinade", "Microwave", "Slow cooker", "Smoked", "Stir fry"]
	return name in types
	
def getRecipe(name):
	page = url.urlopen("http://allrecipes.com/Recipe/"+name+"?scale=24&ismetric=0")
	recipe = {}
	if page:
		soupBody = BeautifulSoup(page)
		recipe["name"] = soupBody.find("h1",{"id":"itemTitle"}).text 
		recipe["ingredients"] = getIngredients(soupBody)
		recipe["directions"] = [i.text for i in soupBody.findAll("span",{"class":"plaincharacterwrap break"})]
		recipe["prepTime"] = soupBody.find("time",{"id":"timePrep"})["datetime"][2:]
		recipe["prepCook"] = soupBody.find("time",{"id":"timeCook"})["datetime"][2:]
		recipe["prepTotal"] = soupBody.find("time",{"id":"timeTotal"})["datetime"][2:]
		recipe["nutritions"] = getNutrients(soupBody)
	return recipe

def Notes():
	text = ["Meat can be replaced with varying degrees of success by tofu, tempeh, seitan, textured vegetable protein, vegetable or nut mixtures"]

if __name__ == "__main__":
	recipes = ["Worlds-Best-Lasagna","Banana-Pancakes-I"]
	for i in recipes:
		print getRecipe(i)