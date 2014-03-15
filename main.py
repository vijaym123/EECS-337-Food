import scrapeData

if __name__=="__main__":
	while True:
		url = raw_input("Enter the all-recipe URL:")
		try :
			name = url[4]
			food = scrapeData(name)
		except:
			print("Eg : http://allrecipes.com/Recipe/Penne-Pasta-with-Cannellini-Beans-and-Escarole/Detail.aspx?evt19=1")
			continue

		while food:
			print "Recipe Name : ", food.recipe["name"]
			print "Enter your choice:"
			print "1) Display Ingredients"
			print "2) Display the ingredients with quantity"
			print "3) Display preparation Time, Cooking time"
			print "4) Display nutritional facts about the recipe"
			choice = raw_input("")
			if choice == '1':
				for i in range(len(food.recipe['ingredients'])):
					print i+1, ")", food.recipe['ingredients'][i]['ingredient']