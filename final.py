import scrapeData

def testURL(url):
	food = scrapeData.Food(url)
	food.tools = []
	food.getTools()
	return food.expectedFormat()