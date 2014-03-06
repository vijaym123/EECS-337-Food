import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json

def getNutrients(soupBody):
	nutrients = {}
	for element in zip([i.find("li",{"class":"categories"}).text for i in soupBody.findAll("ul",{"id":"ulNutrient"})],\
						   [i.find("li",{"class":"units"})for i in soupBody.findAll("ul",{"id":"ulNutrient"})]):
		nutrients[element[0]] = (element[1].span.text, element[1].text[len(element[1].span.text):])
	return nutrients

def getIngredients(soupBody):
	return dict(zip([i.text for i in soupBody.findAll("span",{"id":"lblIngName"})],[ i.text for i in soupBody.findAll("span",{"id":"lblIngAmount"})]))


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

if __name__ == "__main__":
	recipes = ["Worlds-Best-Lasagna","Banana-Pancakes-I"]
	for i in recipes:
		print getRecipe(i)