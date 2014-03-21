import scrapeData

def testURL(url):
	food = scrapeData.Food(url)
	return food.expectedFormat()