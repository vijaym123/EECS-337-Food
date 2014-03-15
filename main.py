import scrapeData
import os
if __name__=="__main__":
	while True:

		url = raw_input("Enter the all-recipe URL : ")
		try :
			name = url.split('/')[4]
			print name
			food = scrapeData.Food(name)
		except:
			print("Eg : http://allrecipes.com/Recipe/Penne-Pasta-with-Cannellini-Beans-and-Escarole/Detail.aspx?evt19=1")
			continue

		while food:
			print "Recipe Name : ", food.recipe["name"]
			print "Enter your choice:"
			print "1) Display Ingredients"
			print "2) Display the ingredients with descriptor"
			print "3) Display the ingredients with quantity"		
			print "4) Display preparation Time, Cooking time"
			print "5) Display nutritional facts about the recipe"
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