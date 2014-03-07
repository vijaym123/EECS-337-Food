import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json
import re
import difflib
import nltk
import fractions
from collections import defaultdict

class Food:
	meatItems = ["Beef","Bison","Dog","Game","Bear","Venison","Wild Boar","Goat",\
				"Horse","Lamb","Mutton","Pork","Rabbit","Turtle","Veal","Chicken", \
				"Cornish Game Hen","Duck","Quail","Turkey","Ostrich","Goose","Bacon",\
				"Salt Beef","Cold cuts","Ham","Sausage", "Alligator","Bison","Frog",\
				"Kangaroo","Lizard","Snake","Insects","Locust","Cricket","Honey Ant",\
				"Grubs","Whale"]
	ingredients = []
	techniques = []
	equipments = []
	measurements = {}
	types = ["Baked","Baking", "Barbecue","Braise", "Camping", "Fermented", "Fried", \
				"Marinade", "Microwave", "Slow cooker", "Smoked", "Stir fry"]

	posTags = dict([("CC","Coordinating conjunction"),("CD","Cardinal number"),("DT","Determiner"),("EX","Existential there"),("FW","Foreign word"),
			("IN","Preposition or subordinating conjunction"),("JJ","Adjective"),("JJR","Adjective, comparative"),("JJS","Adjective, superlative"),
			("LS","List item marker"),("MD","Modal"),("NN","Noun, singular or mass"),("NNS","Noun, plural"),("NNP","Proper noun, singular"),
			("NNPS","Proper noun, plural"),("PDT","Predeterminer"),("POS","Possessive ending"),("PRP","Personal pronoun"),("PRP$","Possessive pronoun"),
			("RB","Adverb"),("RBR","Adverb, comparative"),("RBS","Adverb, superlative"),("RP","Particle"),("SYM","Symbol"),("To","to"),("UH","Interjection"),
			("VB","Verb, base form"),("VBD","Verb, past tense"),("VBG","Verb, gerund or present participle"),
			("VBN","Verb, past participle"),("VBP","Verb, non-rd person singular present"),("VBZ","Verb, rd person singular present"),("WDT","Wh-determiner"),
			("WP","Wh-pronoun"),("WP$","Possessive wh-pronoun"),("WRB","Wh-adverb")])
		
	recipe = {}
	def __init__(self, name, serves = 12):
		self.getAllIngredients()
		self.getAllTechniques() 
		self.getAllEquipments() 
		self.getAllMeasurements()
		self.getRecipe(name, serves)

	def getNutrients(self, soupBody):
		nutrients = {}
		for element in zip([i.find("li",{"class":"categories"}).text for i in soupBody.findAll("ul",{"id":"ulNutrient"})],\
							   [i.find("li",{"class":"units"})for i in soupBody.findAll("ul",{"id":"ulNutrient"})]):
			nutrients[element[0]] = (element[1].span.text, element[1].text[len(element[1].span.text):])
		return nutrients

	def labelIngredients(self, ingredientText, amountText):
		"""
		amount = number + measurement
		ingredient = descriptor + preparation + item
		"""
		tokens = nltk.word_tokenize(ingredientText.replace(",",""))
		tags = nltk.pos_tag(tokens)
		label = defaultdict(list)
		label["ingredient"] = ingredientText
		for i in tags:
			print i
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

	def getIngredients(self, soupBody):
		iterator = zip([i.text for i in soupBody.findAll("span",{"id":"lblIngName"})],[ i.text for i in soupBody.findAll("span",{"id":"lblIngAmount"})])
		return [self.labelIngredients(item[0],item[1]) for item in iterator]

	def meatAndPoultry(self, name):
		"""
		Source wikipedia : http://en.wikibooks.org/wiki/Cookbook:Meat_and_poultry
		Modify this to work on any given item.
		"""
		return difflib.get_close_matches(name,self.meatItems)

	def getAllIngredients(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Cookbook:Ingredients")
		if page:
			soupBody = BeautifulSoup(page)
			self.ingredients = dict([(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})[1:-5]])

	def getAllTechniques(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Category:Cooking_techniques")
		if page:
			soupBody = BeautifulSoup(page)
			self.techniques = dict([ (a.text[9:],a["href"]) for ul in soupBody.findAll("ul")[1:17] for a in ul.findAll("a")])

	def getAllEquipments(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Category:Equipment")
		if page:
			soupBody = BeautifulSoup(page)
			self.equipments = dict([(a.text[9:],a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})])

	def getAllMeasurements(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Cookbook:Units_of_measurement")
		if page:
			soupBody = BeautifulSoup(page)
			test = [(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})]
			self.measurements["volume"] = dict(test[:11])
			self.measurements["weight"] = dict(test[11:17])
			self.measurements["length"] = dict(test[17:21])

	def TypeOfPreparation(self, name):
		return difflib.get_close_matches(name,self.types)
		
	def getRecipe(self, name, serves):
		page = url.urlopen("http://allrecipes.com/Recipe/"+name+"?scale="+str(serves)+"&ismetric=0")
		if page:
			soupBody = BeautifulSoup(page)
			self.recipe["name"] = soupBody.find("h1",{"id":"itemTitle"}).text 
			self.recipe["ingredients"] = self.getIngredients(soupBody)
			self.recipe["directions"] = [i.text for i in soupBody.findAll("span",{"class":"plaincharacterwrap break"})]
			self.recipe["prepTime"] = soupBody.find("time",{"id":"timePrep"})["datetime"][2:]
			self.recipe["prepCook"] = soupBody.find("time",{"id":"timeCook"})["datetime"][2:]
			self.recipe["prepTotal"] = soupBody.find("time",{"id":"timeTotal"})["datetime"][2:]
			self.recipe["nutritions"] = self.getNutrients(soupBody)

	def Notes(self):
		text = ["Meat can be replaced with varying degrees of success by tofu, tempeh, seitan, textured vegetable protein, vegetable or nut mixtures"]

if __name__ == "__main__":
	recipes = ["Worlds-Best-Lasagna","Banana-Pancakes-I"]