import scrapeData
import os
if __name__=="__main__":
	stayInLoop = True
	while stayInLoop == True:

		url = raw_input("Enter the all-recipe URL : ")
		try :
			name = url.split('/')[4]
			print name
			food = scrapeData.Food(url)
		except:
			print("Eg : http://allrecipes.com/Recipe/Penne-Pasta-with-Cannellini-Beans-and-Escarole/Detail.aspx?evt19=1")
			continue

		transformationsDone = [False, False, False, False, False, False]
		while food and stayInLoop == True:
			print "Recipe Name : ", food.recipe["name"]
			print "Enter your choice:"
			print "1) Display Ingredients"
			print "2) Display the ingredients with descriptor"
			print "3) Display the ingredients with quantity"		
			print "4) Display preparation Time, Cooking time"
			print "5) Display nutritional facts about the recipe"
			print "6) Transform to Vegetarian\n7) Transform to Gluten-Free\n8) Transform to Mexican\n9) Transform to Italian\n10) Transform to American\n11) Transform to Very American\n12) Reset Recipe\n13) Exit Program"
			choice = raw_input("")
			os.system('cls' if os.name == 'nt' else 'clear')

			print "\n"
			if choice == '1':
				print "Ingredients are : "
				for i in range(len(food.recipe['ingredients'])):
					print i+1,")", food.recipe['ingredients'][i]['ingredient']
				print "\n"

			elif choice == '2':
				print "Ingredients with descriptor : "
				for i in range(len(food.recipe['ingredients'])):
					print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> descriptor : ", food.recipe['ingredients'][i]['descriptor']
				print "\n"

			elif choice == '3':
				print "Ingredients with quantity : "
				for i in range(len(food.recipe['ingredients'])):
					print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
				print "\n"

			elif choice == '4':
				print "preparation time : ", food.recipe['prepTime']
				print "cooking time : ", food.recipe['prepCook']
				print "\n"

			elif choice == '5':
				for i in food.recipe['nutritions'].keys():
					print  i, " -> ", food.recipe['nutritions'][i][0],food.recipe['nutritions'][i][1]
				print "\n"

			elif choice == '6':
				if transformationsDone[0] == False:
					food.meatReplace()
					transformationsDone[0] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '7':
				if transformationsDone[1] == False:
					food.glutenReplace()
					transformationsDone[1] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '8':
				if transformationsDone[2] == False:
					food.convertCuisine("mexican")
					transformationsDone[2] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '9':
				if transformationsDone[3] == False:
					food.convertCuisine("italian")
					transformationsDone[3] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '10':
				if transformationsDone[4] == False:
					food.convertCuisine("american")
					transformationsDone[4] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '11':
				if transformationsDone[5] == False:
					food.convertCuisine("vamerican")
					transformationsDone[5] = True
					print "\n"
					print "Revised ingredients with quantity: "
					for i in range(len(food.recipe['ingredients'])):
						print i+1,")", food.recipe['ingredients'][i]['ingredient'], " -> quantity : ", food.recipe['ingredients'][i]['amount']
					print "\n\n"
				else:
					print "Transformation already performed\n\n"

			elif choice == '12':
				print "Resetting recipe..."
				del food
				food = scrapeData.Food(url)
				print "Recipe Reset\n\n"
				transformationsDone = [False, False, False, False, False, False]

			elif choice == '13':
				stayInLoop = False
				print "Goodbye!\n\n"

			else:
				print "Not a valid choice.\n\n"






