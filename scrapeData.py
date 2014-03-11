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
import string

class FoodResources:
	meatItems = ["Beef","Bison","Dog","Game","Bear","Venison","Wild Boar","Goat",\
				"Horse","Lamb","Mutton","Fish","Pork","Rabbit","Turtle","Veal","Chicken", \
				"Cornish Game Hen","Duck","Quail","Turkey","Ostrich","Goose","Bacon",\
				"Cold cuts","Ham","Sausage", "Alligator","Bison","Frog",\
				"Kangaroo","Lizard","Snake","Insects","Locust","Cricket","Honey Ant",\
				"Grubs","Whale", "Pepperoni"]
	ingredients = []
	techniques = ["Microwave", "Scald", "Poach", "Broil", "Dice", "Soak", "Beaten", "Caramelization", \
				"Parboil", "Pan broil", "Thermal", "Steam", "Fold", "Roll", "Stew", "Saut", "Roast", \
				"Barbecue", "Beat", "Pressure", "Pickling", "Freeze", "Bast", "Slice", "Boil", "Shirring", \
				"Batter", "Fermentation", "Backyard Grill", "Boiled", "Fry", "Pure", "Toast", "Temper", "Deep Fat Fry", \
				"Roast", "Bake", "Stir-fry", "Scald", "Chiffonade", "Brown", "Mix", "Sweat", "Smoke", "Blanch", "Canning", \
				"Boiling", "Mincing", "Braising", "Grill", "Knead", "Barbecue", "Clay pot", "Simmering", "Microwave", "Pan Fry", "Degorg", "Deglaz"]
	equipments = []
	measurements = {}
	types = ["Baked","Baking", "Barbecue","Braise", "Camping", "Fermented", "Fried", \
				"Marinade", "Microwave", "Slow cooker", "Smoked", "Stir fry", "Grill"]
	
	posTags = dict([("CC","Coordinating conjunction"),("CD","Cardinal number"),("DT","Determiner"),("EX","Existential there"),("FW","Foreign word"),
			("IN","Preposition or subordinating conjunction"),("JJ","Adjective"),("JJR","Adjective, comparative"),("JJS","Adjective, superlative"),
			("LS","List item marker"),("MD","Modal"),("NN","Noun, singular or mass"),("NNS","Noun, plural"),("NNP","Proper noun, singular"),
			("NNPS","Proper noun, plural"),("PDT","Predeterminer"),("POS","Possessive ending"),("PRP","Personal pronoun"),("PRP$","Possessive pronoun"),
			("RB","Adverb"),("RBR","Adverb, comparative"),("RBS","Adverb, superlative"),("RP","Particle"),("SYM","Symbol"),("To","to"),("UH","Interjection"),
			("VB","Verb, base form"),("VBD","Verb, past tense"),("VBG","Verb, gerund or present participle"),
			("VBN","Verb, past participle"),("VBP","Verb, non-rd person singular present"),("VBZ","Verb, rd person singular present"),("WDT","Wh-determiner"),
			("WP","Wh-pronoun"),("WP$","Possessive wh-pronoun"),("WRB","Wh-adverb")])

	vegDict = {'Tofu' : ['sauce', 'soup', 'thai', 'asian', 'tandoori', 'curried', 'curry', 'sautee', 'stirfry', 'fried', 'fry'], 
			    'Mashed Chickpeas' : ['fish', 'seafood'],
				'Seitan': ['brisket', 'medallion', 'cutlet', 'steak', 'filet', 'meatloaf'], 
				'Portobello Mushroom' : ['burger', 'hamburger', 'sandwich'], 
				'Eggplant' : ['lasagna', 'italian', 'pasta', 'stew'],
				'Seitan' : ['chicken']}
	
	glutenDict = [['Cornmeal', ['flour', 'pancake mix']], ['Corn Tortilla', ['bread', 'toast', 'tortilla', 'pita']], ['Zucchini Ribbons', ['lasagna noodle', 'lasagna noodles']], ['Spaghetti Squash', ['spaghetti]']], ['Rice Noodles', ['pasta', 'noodles']], ['Gluten-Free Beer', ['beer', 'ale']], ["Cashews", ['crouton', 'croutons']], ['Gluten-Free Soy Sauce', ['soy sauce']], ['Tofu', ['seitan']] ]

	glutenItems = ["flour", "bread", "toast", "tortilla", "beer", "ale", "cake", "pie", "pasta", "spaghetti", "noodle", "noodles", "lasagna noodle", "lasagna noodles", "pancake", "pancake mix", "pita", "crouton", "croutons", "soy sauce", "seitan"]

	americanDict = [['Cheddar cheese', ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu']]]

	americanItems = ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu']

	veryAmericanDict = [['String cheese', ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu']]]

	veryAmericanItems = ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu']

	conversionCollections = {'american' : americanDict, 'vamerican' : veryAmericanDict}
	conversionChecks = {'american' : americanItems, 'vamerican' : veryAmericanItems}

	# meatReplace = {
	# 	"Beef" : ["seitan","mushroom sause","panner","rice cheese"],
	# 	"Bison" : ["seitan"],
	# 	"Dog" : ["seitan", "textured potato slices"],
	# 	"Game" : ["Stuffed potato", "Stuffed egg"] ,
	# 	"Bear" : ["",""],
	# 	"Venison",
	# 	"Wild Boar",
	# 	"Goat",
	# 	"Horse",
	# 	"Lamb" : ,
	# 	"Mutton" : ["seitan"],
	# 	"Fish" : ["tofu","walnuts","peanuts"],
	# 	"Pork" : ["tofu"],
	# 	"Rabbit",
	# 	"Turtle",
	# 	"Veal",
	# 	"Chicken" : ["tofu"],
	# 	"Cornish Game Hen",
	# 	"Duck" : ["mush"],
	# 	"Quail" ,
	# 	"Turkey" : ["tofu turkey"],
	# 	"Ostrich" ,
	# 	"Goose" ,
	# 	"Bacon" : ["fake bacon bits"],
	# 	"Cold cuts" : ["tofu deli",
	# 	"Ham" : ["smoke flavoring","texture"],
	# 	"Sausage" : ["tofu Sausage"], 
	# 	"Alligator",
	# 	"Bison" ,
	# 	"Frog" ,
	# 	"Kangaroo" : ["tofu turkey"],
	# 	"Lizard",
	# 	"Snake",
	# 	"Insects" : ["deep fried onions"],
	# 	"Locust",
	# 	"Cricket",
	# 	"Honey Ant",
	# 	"Grubs" : ,
	# 	"Whale" : ["seaten", "mushroom sause"]}

	def __init__(self):
		self.getAllIngredients()
		self.getAllTechniques() 
		self.getAllEquipments() 
		self.getAllMeasurements()
		self.meatItems = [i.lower() for i in self.meatItems]

	def getAllIngredients(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Cookbook:Ingredients")
		if page:
			soupBody = BeautifulSoup(page)
			self.ingredients = dict([(a.text,a["href"]) for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})[1:-5]])

	def getAllTechniques(self):
		title = "http://en.wikibooks.org/wiki/"
		page = url.urlopen(title+"Category:Cooking_techniques")
		#if page:
			#soupBody = BeautifulSoup(page)
			#self.techniques = dict([ (a.text[9:],a["href"]) for ul in soupBody.findAll("ul")[1:17] for a in ul.findAll("a")])
		#del self.techniques['']
		#del self.techniques['Recipes/Print version 0 to L']

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

class Food:
	recipe = {}
	resource = None
	tools = []
	serving = 12

	def __init__(self, name, serves = serving):
		self.resource = FoodResources()
		self.getRecipe(name, serves)
		self.getTools()

	def getSummary(self, topic):
		return wikipedia.summary(topic).replace(",","").replace(".","").lower().split(" ")

	def isMeat(self, name):
		"""
		Source wikipedia : http://en.wikibooks.org/wiki/Cookbook:Meat_and_poultry
		Modify this to work on any given item.
		"""
		try :
			if any([ i in self.resource.meatItems for i in name.split(" ")]):
				return True
			#elif any([ i.lower() in self.resource.meatItems for i in self.getSummary(name)]):
			#	return True
			else:
				return False
		except :
			return False

	def getTools(self):
		for step in self.recipe["directions"]:
			self.tools.extend([i for i in self.resource.equipments if i!='' and i.lower() in step.lower()])
		self.tools = list(set(self.tools))

	def getNutrients(self, soupBody):
		nutrients = {}
		for element in zip([i.find("li",{"class":"categories"}).text for i in soupBody.findAll("ul",{"id":"ulNutrient"})],\
							   [i.find("li",{"class":"units"})for i in soupBody.findAll("ul",{"id":"ulNutrient"})]):
			nutrients[element[0]] = (element[1].span.text, element[1].text[len(element[1].span.text):])
		return nutrients

	def removePuncuations(self,stringS):
		pun = string.punctuation
		pun = pun[:2]+pun[3:21]+pun[22:]
		regex=re.compile('[%s]' % re.escape(pun))
		return regex.sub("",stringS)

	def getPrimaryCookingMethods(self):
		tokens = [w.lower() for w in nltk.word_tokenize(self.removePuncuations(" ".join([str(i).lower() for i in self.recipe["directions"]]))) if not w in nltk.corpus.stopwords.words()]
		tags = nltk.pos_tag(tokens)
		tokens = []
		#print self.resource.techniques.keys()
		for i in tags:
			if i[0] in ['cooking', 'bring', 'remaining', 'serving', 'using']:
				continue
			if i[1].startswith("VB") and ( difflib.get_close_matches(i[0],self.resource.types) \
				or difflib.get_close_matches(i[0],self.resource.techniques)):
				tokens.append(i[0])
			elif i[0] in ['grill']:
				tokens.append(i[0])
		tokens = list(set(tokens))
		print tokens

	def labelIngredients(self, ingredientText, amountText):
		"""
		amount = number + measurement
		ingredient = descriptor + preparation + item
		"""
		ingredientText=ingredientText.replace(",","")

		tokens = nltk.word_tokenize(ingredientText)
		tags = nltk.pos_tag(tokens)
		label = defaultdict(list)
		label["ingredient"] = ingredientText

		if difflib.get_close_matches(ingredientText, self.resource.ingredients.keys()):
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

	def TypeOfPreparation(self, name):
		return difflib.get_close_matches(name, self.resource.types)
		
	def getRecipe(self, name, serves):
		page = url.urlopen("http://allrecipes.com/Recipe/"+name+"?scale="+str(serves)+"&ismetric=0")
		if page:
			soupBody = BeautifulSoup(page)
			self.recipe["name"] = soupBody.find("h1",{"id":"itemTitle"}).text 
			self.recipe["description"] = soupBody.find("meta",{"id":"metaDescription"})["content"]
			self.recipe["ingredients"] = self.getIngredients(soupBody)
			self.recipe["directions"] = [i.text for i in soupBody.findAll("span",{"class":"plaincharacterwrap break"})]
			self.recipe["prepTime"] = soupBody.find("time",{"id":"timePrep"})["datetime"][2:]
			self.recipe["prepCook"] = soupBody.find("time",{"id":"timeCook"})["datetime"][2:]
			self.recipe["prepTotal"] = soupBody.find("time",{"id":"timeTotal"})["datetime"][2:]
			self.recipe["nutritions"] = self.getNutrients(soupBody)

	def meatReplace(self):
		for item in self.recipe["ingredients"]:
			if self.isMeat(item["item"]):
				replacer = self.findVegReplacer(item["item"])
				replacer = self.alreadyThere(replacer)
				if replacer in "Portobello Mushroom":
					print item["number"], " ", item["measurement"], " ", item["item"]," Replace with : ", self.serving, replacer, "(s)"
					item["item"] = replacer
					item["measurement"] = ""
					item["number"] = self.serving
				else:
					print item["number"], " ", item["measurement"], " ", item["item"]," Replace with : ", item["number"], item["measurement"], replacer
					item["item"] = replacer
					item["number"] = self.serving

	def alreadyThere(self, newThing):
		for item in self.recipe["ingredients"]:
			if newThing in item["item"]:
				if newThing in "Eggplant":
					return "Zucchini"
				#ADD MORE FALLBACKS HERE
		return newThing

	
	def findVegReplacer(self, name):
		for replacement in self.resource.vegDict.keys():
			for keyword in self.resource.vegDict[replacement]:
				if keyword in str(self.recipe["description"]).lower().split(" ") or keyword in str(self.recipe["name"]).lower().split(" "):
					return replacement
		return "Tofu"

	def glutenReplace(self):
		for item in self.recipe["ingredients"]:
			if self.hasGluten(item["item"]):
				replacer = self.findGlutenReplacer(item["item"])
				print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"], " ", item["measurement"], " ", replacer
				item["item"] = replacer
				item["number"] = self.serving

	def findGlutenReplacer(self, name):
		for replacement in self.resource.glutenDict:
			for keyword in replacement[1]:
				if keyword == name:
					return replacement[0]

	
	def hasGluten(self, name):
		"""
		Source wikipedia : http://en.wikibooks.org/wiki/Cookbook:Meat_and_poultry
		Modify this to work on any given item.
		"""
		try :
			if any([ i in self.resource.glutenItems for i in name.split(" ")]):
				return True
			else:
				for i in self.resource.glutenItems:
					if name == i:
						return True
				return False
		except :
			return False


	def convertCuisine(self, conversion): 
		for item in self.recipe["ingredients"]:
			if self.shouldBeConverted(item["item"], conversion):
				replacer = self.findConversion(item["item"], conversion)
				if replacer.lower() == 'string cheese':
					item["number"] = 20*item["number"]
					item["measurement"] = "sticks"
				print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"], " ", item["measurement"], " ", replacer
				item["item"] = replacer
				item["number"] = self.serving
				

	def findConversion(self, name, dictChoice):
		for replacement in self.resource.conversionCollections[dictChoice]:
			print replacement[0]
			for keyword in replacement[1]:
				if keyword == name:
					return replacement[0]

	def shouldBeConverted(self, name, checkChoice):
		try :
			if any([ i in self.resource.conversionChecks[checkChoice] for i in name.split(" ")]):
				return True
			else:
				for i in self.resource.conversionChecks[checkChoice]:
					if name == i:
						return True
				return False
		except :
			return False


	def Notes(self):
		text = ["Meat can be replaced with varying degrees of success by tofu, tempeh, seitan, textured vegetable protein, vegetable or nut mixtures"]

if __name__ == "__main__":
	recipes = ["Best-Burger-Ever","Worlds-Best-Lasagna","Banana-Pancakes-I"]
	k=Food(recipes[0])
	k.getPrimaryCookingMethods()
	recipes = ["Best-Burger-Ever","Worlds-Best-Lasagna","Banana-Pancakes-I","Creamy-Banana-Bread"]
	k=Food("Worlds-Best-Lasagna")
	#k.meatReplace()
	k.convertCuisine('vamerican')