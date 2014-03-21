import scrapeData
import os
import pprint
import copy
import urllib2 as url
from bs4 import BeautifulSoup

def outputRecipie(link):
	output = {}
	food = None
	food = scrapeData.Food(link)
	output["ingredients"] = copy.deepcopy(food.recipe['ingredients'])
	output["tools"] = copy.deepcopy(food.tools)
	output["cooking methods"] = copy.deepcopy(food.getCookingMethods())
	output["primary methods"] = copy.deepcopy(food.getPrimaryMethod(food.getCookingMethods()))

	food.meatReplace()
	output["after meat replace"] = copy.deepcopy(food.recipe["ingredients"])
	food.recipe["ingredients"] = copy.deepcopy(output["ingredients"])

	food.glutenReplace()
	output["after gluten replace"] = copy.deepcopy(food.recipe["ingredients"])
	food.recipe["ingredients"] = copy.deepcopy(output["ingredients"])

	food.convertCuisine("mexican")
	output["mexican"] = copy.deepcopy(food.recipe["ingredients"])
	food.recipe["ingredients"] = copy.deepcopy(output["ingredients"])

	food.convertCuisine("italian")
	output["italian"] = copy.deepcopy(food.recipe["ingredients"])
	food.recipe["ingredients"] = copy.deepcopy(output["ingredients"])


	food.convertCuisine("american")
	output["american"] = copy.deepcopy(food.recipe["ingredients"])
	food.recipe["ingredients"] = copy.deepcopy(output["ingredients"])


	food.convertCuisine("vamerican")
	output["vamerican"] = copy.deepcopy(food.recipe["ingredients"])
	return output

if __name__ == "__main__":
	number = 1
	maxNumber = 10
	Types = ["breakfast-and-brunch","main-dish"]
	t = Types[1]
	page = url.urlopen("http://allrecipes.com/recipes/"+t+"/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
	recipeNames = []

	while page:
		print number
		soupBody = BeautifulSoup(page)
		recipeNames.extend([ [i.find('a').text, { "url" : i.find('a')["href"], "output" : outputRecipie(i.find('a')["href"]) } ] for i in soupBody.findAll('h3',{"class":"resultTitle"})])
		number = number + 1
		page = url.urlopen("http://allrecipes.com/recipes/"+t+"/main.aspx?evt19=1&vm=l&p34=HR_ListView&Page="+str(number))
		if number >= maxNumber:
			break

		for recipe in recipeNames:
			filename = "./recipeData/"+recipe[0]+".data"
			with open(filename, "w") as fout:
				fout.write(pprint.pformat(recipe[1]))
		recipeNames = []
