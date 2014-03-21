import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json
import re
import difflib
import nltk
import fractions
from collections import defaultdict
import string

class FoodResources:
	meatItems = ["Beef","Bison","Dog","Game","Bear","Venison","Wild Boar","Goat",\
				"Horse","Lamb","Mutton","Fish", "Salmon", "Sea Bass", "Tuna", "Shark", "Mahi-Mahi", "Pork","Rabbit","Turtle","Veal","Chicken", \
				"Cornish Game Hen","Duck","Quail","Turkey","Ostrich","Goose","Bacon","Steak",\
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
	equipments = ['grill', 'knife', 'bowl', 'refridgerator', 'oven', 'microwave', 'frying pan', 'plate', 'cutting board', 'fork', 'spoon', \
				'blender', 'rolling pin', 'sink', 'freezer', 'baking dish', 'foil', 'griddle', 'skillet', 'dish', 'apple corer', 'apple cutter' \
				'baster' 'biscuit cutter', 'bottle opener', 'bread knife', 'browning tray', 'butter curler', 'cheese knife', 'cheesecloth', \
				'cherry pitter', 'chinoise', 'oclander', 'corkscrew', 'crab cracker', 'dough scraper', 'egg piercer', 'egg poacher', 'egg separator', \
				'egg slicer', 'egg timer', 'fillet knife', 'fish scaler', 'sifter', 'funnel', 'garlic press', \
				'grapefruit knife', 'grater', 'ladle', 'lame', 'lemon squeezer', 'lobster fork', 'lobster pick', \
				'mandoline', 'colander pot', 'measuring jug', 'measuring spoon', 'measuring cup', 'meat grinder', \
				'meat tenderiser', 'meat thermometer', 'melon baller', 'mezzaluna', 'nutcracker', 'oven glove', \
				'oven mitt', 'pastry bag', 'pastry brush', 'basting brush', 'pizza shovel', 'peeler', 'pepper mill', \
				'potato masher', 'pizza cutter', 'pot holder', 'poultry shears', 'ricer', 'roller docker', \
				'rolling pin', 'salt shaker', 'scales', 'scissors', 'scoop', 'sieve', 'slotted spoon', 'spatula', \
				'spider', 'tamis', 'tongs', 'whisk', 'wooden spoon', 'zester', 'casserole pan', 'griddle', 'hot plate', \
				'sauce pan', 'sautee pan', 'stockpot', 'pressure cooker', 'wok', 'wonder pot', 'food processor', \
				'cookie sheet']
	measurements = {}
	types = ["Baked","Baking", "Barbecue","Braise", "Camping", "Fermented", "Fried", "Fry", \
				"Marinade", "Microwave", "Slow cooker", "Smoked", "Stir fry", "Grill"]
	
	posTags = dict([("CC","Coordinating conjunction"),("CD","Cardinal number"),("DT","Determiner"),("EX","Existential there"),("FW","Foreign word"),
			("IN","Preposition or subordinating conjunction"),("JJ","Adjective"),("JJR","Adjective, comparative"),("JJS","Adjective, superlative"),
			("LS","List item marker"),("MD","Modal"),("NN","Noun, singular or mass"),("NNS","Noun, plural"),("NNP","Proper noun, singular"),
			("NNPS","Proper noun, plural"),("PDT","Predeterminer"),("POS","Possessive ending"),("PRP","Personal pronoun"),("PRP$","Possessive pronoun"),
			("RB","Adverb"),("RBR","Adverb, comparative"),("RBS","Adverb, superlative"),("RP","Particle"),("SYM","Symbol"),("To","to"),("UH","Interjection"),
			("VB","Verb, base form"),("VBD","Verb, past tense"),("VBG","Verb, gerund or present participle"),
			("VBN","Verb, past participle"),("VBP","Verb, non-rd person singular present"),("VBZ","Verb, rd person singular present"),("WDT","Wh-determiner"),
			("WP","Wh-pronoun"),("WP$","Possessive wh-pronoun"),("WRB","Wh-adverb")])

	vegDict = {'Eggplant' : ['lasagna', 'italian', 'pasta', 'stew'], 
				'Tofu' : ['eel', 'shrimp', 'lobster', 'crab', 'soup', 'thai', 'asian', 'tandoori', 'curried', 'curry', 'sautee', 'stirfry', 'fried', 'fry'], 
			    'Mashed Chickpeas' : ['anchovy', 'anchovies', 'sardine', 'sardines', 'fish', 'seafood'],
				'Seitan': ['chicken', 'pork', 'bass', 'cod', 'catfish', 'blowfish', 'herring', 'halibut', 'mackerel', 'mahi mahi', 'monkfish', 'pike', 'salmon', 'sea bass', 'shark', 'snapper', 'swordfish', 'tilapia', 'trout', 'tuna', 'brisket', 'medallion', 'cutlet', 'steak', 'steaks', 'filet', 'meatloaf', 'ground beef'], 
				'Portobello Mushroom' : ['burger', 'hamburger', 'sandwich', 'breast', 'boneless']}
	
	glutenDict = {'Cornmeal' : ['flour', 'pancake mix'],
					'Corn Tortilla' : ['bread', 'toast', 'tortilla', 'pita'],
					'Zucchini Ribbons' : ['lasagna noodle', 'lasagna noodles'],
					'Spaghetti Squash': ['spaghetti]'],
					'Rice Noodles' : ['pasta', 'noodles','macaroni', 'rotelli', 'Acini di Pepe', 'Alphabet Pasta', 'Anelli', 'Bucatini', 'Campanelle', 'Cappelletti', 'Casarecce', 'Cavatappi', 'Cavatelli', 'Conchiglie', 'Ditalini', 'Macaroni', 'Farfalle', 'Farfalline', 'Fideo', 'Fusilli', 'Gemelli', 'Gigli', 'Linguine', 'Manicotti', 'Orecchiette', 'Orzo', 'Penne', 'Mostaccioli', 'Penne Rigate', 'Penne', 'Radiatori', 'Ravioli', 'Reginette', 'Riccioli',  'Rigatoni', 'Rocchetti', 'Rotelle', 'Rotini', 'Ruote', 'Spaghetti', 'Tortellini', 'Tortiglioni', 'Tripolini', 'Tubini', 'Vermicelli', 'Ziti'],
					'Gluten-Free Beer' : ['beer', 'ale'],
					'Cashews' : ['crouton', 'croutons', 'breadcrumbs', 'bread crumbs', 'crumbs'],
					'Gluten-Free Soy Sauce' : ['soy sauce'],
					'Tofu': ['seitan']}

	glutenItems = ["breadcrumbs", "bread crumbs", "crumbs", "Acini di Pepe", "Alphabet Pasta", "Anelli", "Bucatini", "Campanelle", "Cappelletti", "Casarecce", "Cavatappi", "Cavatelli", "Conchiglie", "Ditalini", "Macaroni", "Farfalle", "Farfalline", "Fideo", "Fusilli", "Gemelli", "Gigli", "Linguine", "Manicotti", "Orecchiette", "Orzo", "Penne", "Mostaccioli", "Penne Rigate", "Penne", "Radiatori", "Ravioli", "Reginette", "Riccioli",  "Rigatoni", "Rocchetti", "Rotelle", "Rotini", "Ruote", "Spaghetti", "Tortellini", "Tortiglioni", "Tripolini", "Tubini", "Vermicelli", "Ziti", "flour", "bread", "toast", "tortilla", "beer", "ale", "cake", "pie", "pasta", "spaghetti", "noodle", "noodles", "lasagna noodle", "lasagna noodles", "pancake", "pancake mix", "pita", "crouton", "croutons", "soy sauce", "seitan"]

	americanDict = {'broccoli' : ['greens', 'green vegetables', 'asparagus'],
                        'French Fries' : ['potatoes', 'root vegetables'],
                        'Cheddar cheese' : ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu'],
                        'Ground Beef' : ['chicken', 'pork', 'steak', 'fish'],
                        'ketchup' : ['tomato sauce'],
                        'Tabasco sauce' : ['hot sauce'],
                        'instant noodles' : ['noodles'],
                        'instant pasta' : ['pasta']}

	americanItems = ['pasta', 'noodles', 'hot sauce', 'tomato sauce', 'asparagus', 'greens', 'green vegetables', 'potatoes', 'root vegetables', 'parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu', 'chicken', 'pork', 'steak', 'fish']

	veryAmericanDict = {'Grease' : ['vegetable oil'],
                            'American Fries' : ['potatoes', 'potato', 'vegetable', 'vegetables'],
                            'ketchup' : ['tomatoes', 'tomato'],
                            'mustard' : ['hot sauce'],
                            'String Cheese' : ['cheese', 'cheddar', 'cheddar cheese', 'feta', 'feta cheese', 'parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu'],
                            'Bacon' : ['chicken', 'pork', 'steak', 'fish'],
                            'Mayonaisse' : ['sauce'],
                            'SpaghettiO\'s' : ['spaghetti', 'acini di pepe', 'alphabet pasta', 'anelli', 'bucatini', 'campanelle', 'cappelletti', 'casarecce', 'cavatappi', 'cavatelli', 'conchiglie', 'ditalini', 'macaroni', 'farfalle', 'farfalline', 'fideo', 'fusilli', 'gemelli', 'gigli', 'linguine', 'manicotti', 'orecchiette', 'orzo', 'penne', 'mostaccioli', 'penne rigate', 'radiatori', 'ravioli', 'reginette', 'riccioli',  'rigatoni', 'rocchetti', 'rotelle', 'rotini', 'ruote', 'spaghetti', 'tortellini', 'tortiglioni', 'tripolini', 'tubini', 'vermicelli', 'ziti'],
                            'hot dog bun' : ['bread loaf', 'croissant'],
                            'hamburger bun' : ['bagel'],
                            'Instant Mac and Cheese' : ['noodles'],
                            'peanut butter' : ['nuts', 'walnuts', 'almonds', 'peanuts'],
                            'canned fruit' : ['fruit'],
                            'canned apples' : ['apples'],
                            'frozen broccoli' : ['broccoli', 'fresh broccoli'],
                            'frozen carrots' : ['carrots', 'fresh carrots'],
                            'frozen peas' : ['peas', 'fresh peas'],
                            'frozen corn' : ['corn', 'fresh corn'],
                            'full-fat milk' : ['low-fat milk', 'non-fat-milk']}

	veryAmericanItems = ['vegetable oil', 'cheese', 'cheddar', 'cheddar cheese', 'feta', 'feta cheese', 'acini di pepe', 'peas', 'fresh peas', 'corn', 'fresh corn', 'broccoli', 'carrots', 'fresh broccoli', 'fresh carrots', 'alphabet pasta', 'anelli', 'bucatini', 'campanelle', 'cappelletti', 'casarecce', 'cavatappi', 'cavatelli', 'conchiglie', 'ditalini', 'macaroni', 'farfalle', 'farfalline', 'fideo', 'fusilli', 'gemelli', 'gigli', 'linguine', 'manicotti', 'orecchiette', 'orzo', 'penne', 'mostaccioli', 'penne rigate', 'radiatori', 'ravioli', 'reginette', 'riccioli',  'rigatoni', 'rocchetti', 'rotelle', 'rotini', 'ruote', 'spaghetti', 'tortellini', 'tortiglioni', 'tripolini', 'tubini', 'vermicelli', 'ziti', 'hot sauce', 'non-fat milk', 'low-fat milk', 'apples', 'fruit', 'walnuts', 'almonds', 'peanuts', 'nuts', 'noodles', 'potato', 'tomato', 'vegetable', 'tomatoes', 'bagel', 'croissant', 'bread loaf', 'spaghetti', 'potatoes', 'vegetables', 'parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu', 'chicken', 'pork', 'steak', 'fish', 'sauce', 'Mayonaisse']

	mexicanDict = {'Pepperjack cheese' : ['parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu', 'cheddar', 'cheddar cheese'],
					'Ground Beef' : ['chicken', 'pork', 'fish', 'ham', 'turkey'],
					'Carne Asada' : ['steak'],
					'Chorizo' : ['sausage', 'bratwurst', 'kielbasa', 'bacon', 'salami', 'pepperoni', 'italian sausage'],
					'Salsa' : ['hot sauce'],
					'Corn' : ['broccoli', 'peas', 'pea', 'greens', 'mixed greens'],
					'Potatoes' : ['beets', 'beet', 'roots', 'root vegetables', 'turnip', 'turnips', 'watercress'],
					'Onion' : ['asparagus', 'spinach', 'celery', 'spring onion'],
					'Lettuce' : ['kale', 'cabbage', 'brussels sprout', 'seaweed', 'sea kale', 'sea beets', 'sea vegetables'],
					'Bell Pepper' : ['carrot', 'carrots', 'arugula'],
					'Tomato' : ['olive', 'olives', 'kalamata olives', 'pumpkin', 'pumpkins'],
					'Avocado' : ['bok choy', 'yao choy', 'pak choy', 'gourd', 'gourds', 'squash', 'melon', 'melons', 'cantelope'],
					'Pico de Gallo' : ['sauce'],
					'Guacomole' : ['hummus', 'chickpeas', 'garbanzo beans'],
					'Chipotle Mayonaisse' : ['mayonaisse', 'mayo'],
					'Tortilla' : ['bread', 'white bread', 'pita', 'roll', 'rolls', 'dinner rolls',  'scone', 'scones', 'biscuit', 'biscuits']}

	mexicanItems = ['roll', 'rolls', 'dinner rolls', 'scone', 'scones', 'biscuit', 'seaweed', 'sea kale', 'sea beets', 'sea vegetables', 'biscuits', 'bok choy', 'kale', 'greens', 'hummus', 'chickpeas', 'garbanzo beans', 'mixed greens', 'celery', 'brussels sprout', 'cabbage', 'spring onion', 'olive', 'cabbage', 'kalamata olives', 'olives','pea', 'pak choy', 'turnip', 'turnips', 'watercress', 'peas', 'spinach', 'beet', 'beets', 'squash', 'pumpkin', 'pumpkins', 'melons', 'melon', 'cantelope', 'gourd', 'gourds', 'roots', 'root vegetables', 'yao choy', 'carrot', 'arugula', 'carrots', 'broccoli', 'asparagus', 'hot sauce', 'parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'mozzarella cheese', 'mozzarella', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'cheddar cheese', 'bleu', 'chicken', 'pork', 'steak', 'fish', 'bratwurst', 'kielbasa', 'bacon', 'mayonnaise', 'mayo', 'sauce', 'bread', 'white bread', 'pita', 'sausage', 'salsa', 'ham', 'turkey', 'salami', 'pepperoni', 'italian sausage']

	italianDict = {'Parmigiano-Reggiano' : ['parmesan cheese'],
					'Mozzarella' : ['swiss cheese', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu'],
					'Italian Sausage' : ['ground beef', 'sausage', 'chorizo', 'kielbasa', 'bratwurst'],
					'Marinara Sauce' : ['ketchup'],
					'Spaghetti' : ['noodles', 'udon', 'udon noodles', 'ramen', 'ramen noodles', 'lo mein', 'lo mein noodles'],
					'Risotto' : ['rice'],
					'Eggplant' : ['squash', 'melon', 'melons', 'pumpkin', 'pumpkins', 'cantelope'],
					'Tomato' : ['gourd', 'gourds'],
					'Carrots' : ['corn'],
					'Artichoke' : ['bok choy', 'pak choy', 'yao choy'],
					'Onion' : ['leek', 'leeks', 'spring onions'],
					'Lentils' : ['endives', 'endive'],
					'Broccoli' : ['cabbage', 'brussels sprouts', 'brussels sprouts', 'new zealand cabbage'],
					'Chickpeas' : ['refried beans', 'hummus'],
					'Kale' : ['orache', 'orach', 'atriplex'],
					'Thyme' : ['dill'],
					'Olive oil' : ['vegetable oil', 'oil'],
					'Ciabatta' : ['roll', 'rolls', 'dinner rolls', 'bread', 'scone', 'scones', 'biscuit', 'biscuits'],
					'Bay Leaves' : ['ginseng', 'ginger', 'star-of-anise', 'garam masala', 'curry powder', 'sambar', 'sambar powder'],
					'Spinach' : ['seaweed', 'sea vegetables', 'sea beets', 'beets']}

	italianItems = ['squash', 'roll', 'rolls', 'new zealand cabbage', 'seaweed', 'sea vegetables', 'sea beets', 'beets', 'dinner rolls', 'bread', 'ginseng', 'ginger', 'star-of-anise', 'garam masala', 'curry powder', 'sambar', 'sambar powder', 'scone', 'scones', 'biscuit', 'biscuits', 'orache', 'orach', 'oil', 'vegetable oil', 'dill', 'atripplex', 'melon', 'cabbage', 'brussels sprout', 'brussels sprouts', 'melons', 'leek', 'leeks', 'endive', 'refried beans', 'hummus', 'endives', 'spring onions', 'pumpkin', 'pumpkins', 'cantelope', 'bok choy', 'pak choy', 'yao choy', 'gourd', 'gourds', 'corn', 'parmesan cheese', 'parmigiano-reggiano', 'swiss cheese', 'manchego cheese', 'manchego', 'monterrey jack cheese', 'monterrey jack', 'gouda cheese', 'gouda', 'bleu cheese', 'bleu', 'Italian Sausage', 'ground beef', 'ketchup', 'sausage', 'chorizo', 'kielbasa', 'bratwurst', 'noodles', 'udon', 'udon noodles', 'ramen', 'ramen noodles', 'lo mein', 'lo mein noodles', 'rice']


	conversionCollections = {'american' : americanDict, 'vamerican' : veryAmericanDict, 'mexican' :mexicanDict, 'italian' :italianDict}
	conversionChecks = {'american' : americanItems, 'vamerican' : veryAmericanItems, 'mexican' : mexicanItems, 'italian' : italianItems}

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
			self.equipments.extend([a.text[9:] for a in soupBody.findAll('a', attrs = {'href' : re.compile('/wiki/Cookbook:*')})])

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
			nameList = []
			for i in name.split(" "):
				try:
					nameList.append(i.lower())
				except:
					pass
			if any([ i in self.resource.meatItems for i in nameList]):
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

		length = len(self.tools)-1
		incI = True

		i = 0
		while i <= length:
			incI = True
			j = i+1
			while j <= length:
				if (self.tools[i]).lower() in (self.tools[j]).lower():
					del self.tools[i]
					length = length - 1
					incI = False
				elif (self.tools[j]).lower() in (self.tools[i]).lower():
					del self.tools[j]
					length = length - 1
				j = j+1
			if incI == True:
				i = i + 1		


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

	def getCookingMethods(self):
		tokens = [w.lower() for w in nltk.word_tokenize(self.removePuncuations(" ".join([str(i).lower() for i in self.recipe["directions"]]))) if not w in nltk.corpus.stopwords.words()]
		#print tokens
		tags = nltk.pos_tag(tokens)
		#print tags
		tokens = []
		#print self.resource.techniques.keys()
		for i in tags:
			if i[0] in ['cooking', 'bring', 'remaining', 'serving', 'using']:
				continue
			if i[1].startswith("VB") and ( difflib.get_close_matches(i[0],self.resource.types) \
				or difflib.get_close_matches(i[0],self.resource.techniques)):
				tokens.append(i[0])
			elif i[0] in ['grill', 'fry', 'heat', 'bake', 'barbecue', 'braise', 'ferment', 'marinade', 'microwave', 'cook', 'smoke', 'stirfry']:
				tokens.append(i[0])
		tokens = list(set(tokens))
		return tokens

	def getPrimaryMethod(self, methods):
		hierarchy = ['bake', 'grill', 'fry', 'roast', 'smoke', 'boil', 'sautee', 'broil' 'steam', 'heat', 'mix', 'stir']
		bestIndex = 99
		for method in methods:
			for i in range(0, len(hierarchy)):
				if method.lower() in hierarchy[i]:
					if i < bestIndex:
						bestIndex = i
		if bestIndex == 99:
			return methods[0]
		return hierarchy[bestIndex]

	def labelIngredients(self, ingredientText, amountText):
		"""
		amount = number + measurement
		ingredient = descriptor + preparation + item
		"""
		ingredientText=ingredientText.replace(",","")

		tokens = nltk.word_tokenize(self.convertToAscii(ingredientText))
		tags = nltk.pos_tag(tokens)
		label = defaultdict(list)
		label["ingredient"] = self.convertToAscii(ingredientText)

		if difflib.get_close_matches(label["ingredient"], self.resource.ingredients.keys()):
			label["item"].append(label["ingredient"])
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
		data = soupBody.findAll("p",{"itemprop":"ingredients"})
		iterator = []
		for i in data:
			if i.find('span',{"class":"ingredient-name"}) and self.convertToAscii(i.find('span',{"class":"ingredient-name"}).text)!='':
				if i.find('span',{"class":"ingredient-amount"}):
					iterator.append((i.find('span',{"class":"ingredient-name"}).text,i.find('span',{"class":"ingredient-amount"}).text))
				else :
					iterator.append((i.find('span',{"class":"ingredient-name"}).text,""))
		return [self.labelIngredients(item[0],item[1]) for item in iterator]

	def TypeOfPreparation(self, name):
		return difflib.get_close_matches(name, self.resource.types)
	
	def convertToAscii(self,s):
		output = []
		for word in s.split(" "):
			try :
				output.append(str(word))
			except:
				pass
		return " ".join(output)

	def getRecipe(self, name, serves):
		page = url.urlopen(name+"?scale="+str(serves)+"&ismetric=0")
		if page:
			soupBody = BeautifulSoup(page)
			self.recipe["name"] = soupBody.find("h1",{"id":"itemTitle"}).text 
			self.recipe["description"] = soupBody.find("meta",{"id":"metaDescription"})["content"]
			self.recipe["ingredients"] = self.getIngredients(soupBody)
			self.recipe["directions"] = [self.convertToAscii(i.text) for i in soupBody.findAll("span",{"class":"plaincharacterwrap break"})]
			self.recipe["prepTime"] = soupBody.find("time",{"id":"timePrep"})["datetime"][2:]
			self.recipe["prepCook"] = soupBody.find("time",{"id":"timeCook"})["datetime"][2:]
			self.recipe["prepTotal"] = soupBody.find("time",{"id":"timeTotal"})["datetime"][2:]
			self.recipe["nutritions"] = self.getNutrients(soupBody)

	def meatReplace(self):
		for item in self.recipe["ingredients"]:
			if self.isMeat(item["ingredient"]):
				replacer = self.findVegReplacer(item["item"])
				replacer = self.alreadyThere(replacer)
				if 'sauce' in (item["item"]).lower():
					replacer = item["item"]
				elif 'broth' in (item["item"]).lower():
					replacer = "Vegetable Broth"
				elif 'breast' in (item["item"]).lower():
					print item["number"], " ", item["measurement"], " ", item["item"]," Replace with : ", self.serving, "Portobello Mushroom(s)"
					item["item"] = "Portobello Mushroom"
					item["ingredient"] = "Portobello Mushroom"
				elif replacer in "Portobello Mushroom":
					print item["number"], " ", item["measurement"], " ", item["item"]," Replace with : ", self.serving, replacer, "(s)"
					item["item"] = replacer
					item["ingredient"] = replacer
					item["measurement"] = ""
					item["number"] = self.serving
					item["amount"] = self.serving
				else:
					print item["number"], " ", item["measurement"], " ", item["item"]," Replace with : ", item["number"], item["measurement"], replacer
					item["item"] = replacer
					item["ingredient"] = replacer
					item["number"] = self.serving
				item["amount"] = str(item["number"]) + " " + item["measurement"]

	def alreadyThere(self, newThing):
		for item in self.recipe["ingredients"]:
			if newThing in item["item"]:
				if newThing in "Eggplant":
					return "Zucchini"
				#if newThing.lower() in "pepperjack cheese":
				#	return "Cheddar Cheese"
				#ADD MORE FALLBACKS HERE
		return newThing

	
	def findVegReplacer(self, name):
		for replacement in self.resource.vegDict.keys():
			for keyword in self.resource.vegDict[replacement]:
				#if name.lower() in keyword.lower() or keyword.lower() in name.lower():
				if keyword.lower() in str(self.recipe["description"]).lower().split(" ") or keyword.lower() in str(self.recipe["name"]).lower().split(" "):
					return replacement
		return "Tofu"

	def glutenReplace(self):
		for item in self.recipe["ingredients"]:
			if self.hasGluten(item["item"]):
				replacer = self.findGlutenReplacer(item["item"])
				print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"], " ", item["measurement"], " ", replacer
				item["item"] = replacer
				item["ingredient"] = replacer
				item["number"] = self.serving

	def findGlutenReplacer(self, name):
		for replacement in self.resource.glutenDict:
			for keyword in (self.resource.glutenDict)[replacement]:
				if keyword.lower() in name.lower():
					return replacement

	
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
			item["item"] = item["item"].lower()
			if "broth" in item["item"]:
				#do nothing for now
				a = 1 + 1
			elif self.shouldBeConverted(item["item"], conversion):
				replacer = str(self.findConversion(item["item"], conversion))
				replacer = self.alreadyThere(replacer)
				if replacer == 'String Cheese':
					print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"]*20, " ", "sticks", " ", replacer
					item["number"] = 20*item["number"]
					item["measurement"] = "sticks"
				elif (replacer in "ketchup") or (replacer in "Mayonaisse") or (replacer in "Tabasco sauce"):
					print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"], " ", "bottles", " ", replacer
					item["measurement"] = "bottles"
				elif item["number"] != 0:
					print item["number"], " ", item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["number"], " ", item["measurement"], " ", replacer
				else:
					print item["measurement"], " ", item["item"], " --> REPLACE WITH: ", item["measurement"], " ", replacer
				item["item"] = replacer
				item["ingredient"] = replacer
			item["amount"] = str(item["number"]) + " " + item["measurement"]

	def findConversion(self, name, dictChoice):
		for replacement in self.resource.conversionCollections[dictChoice]:
			for keyword in (self.resource.conversionCollections[dictChoice])[replacement]:
				if keyword.lower() in name.lower():
					return replacement

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

	def expectedFormat(self):
		output = {}
		output["ingredients"] = []
		for item in self.recipe["ingredients"]:
			test = {}
			test["name"] = item["item"]
			test["quantity"] = item["number"]
			test["measurement"] = item["measurement"]
			test["descriptor"] = item["descriptor"]
			test["preparation"] = item["preparation"]
			output["ingredients"].append(test)
		output["cooking method"] = self.getPrimaryMethod(self.getCookingMethods())
		output["cooking tools"] = self.tools
		return output


if __name__ == "__main__":
	
	'''
	#recipes = ["Best-Burger-Ever","Worlds-Best-Lasagna","Banana-Pancakes-I","Creamy-Banana-Bread"]
	k=Food("http://allrecipes.com/Recipe/worlds-best-lasagna")
	k.getCookingMethods()
	print k.tools
	k.meatReplace()
	#k.convertCuisine('italian')
	'''
	
	u = raw_input("Enter AllRecipes.com URL: ")
	print "\n\n"
	k = Food(u)
	k.getCookingMethods()
	stayInLoop = True
	transformationsDone = [False, False, False, False, False, False]
	while stayInLoop == True:
		print "What transformation would you like to perform on your recipe?\n1) To Vegetarian\n2) To Gluten-Free\n3) To Mexican\n4) To Italian\n5) To American\n6) To Very American\n7) Reset Recipe\n8) Exit Program"
		choice = raw_input("TYPE THE NUMBER OF THE TRANSFORMATION YOU WOULD LIKE TO PERFORM AND PRESS \"ENTER\": ")
		if choice == "1":
			if transformationsDone[0] == False:
				k.meatReplace()
				transformationsDone[0] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "2":
			if transformationsDone[1] == False:
				k.glutenReplace()
				transformationsDone[1] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "3":
			if transformationsDone[2] == False:
				k.convertCuisine("mexican")
				transformationsDone[2] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "4":
			if transformationsDone[3] == False:
				k.convertCuisine("italian")
				transformationsDone[3] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "5":
			if transformationsDone[4] == False:
				k.convertCuisine("american")
				transformationsDone[4] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "6":
			if transformationsDone[5] == False:
				k.convertCuisine("vamerican")
				transformationsDone[5] = True
				print "\n\n"
			else:
				print "Transformation already performed\n\n"
		elif choice == "7":
			del k
			k = Food(u)
			print "Recipe Reset\n\n"
			transformationsDone = [False, False, False, False, False, False]
		elif choice == "8":
			stayInLoop = False
			print "Goodbye!\n\n"
		else:
			print "Not a valid transformation.\n\n"

	







