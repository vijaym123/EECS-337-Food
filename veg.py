import urllib2 as url
from bs4 import BeautifulSoup
import sys
import json

vegetarian = []

vegetarian.append(["Tofu", ["sauce", "soup", "thai", "asian", "tandoori", "curried", "curry", "sautee", "stirfry", "fried", "fry"]])

vegetarian.append(["Mashed Chickpeas", ["fish", "seafood"]])

vegetarian.append(["Seitan", ["chicken", "brisket", "medallion", "cutlet", "steak", "filet"]])

vegetarian.append(["Portobello Mushroom", ["burger", "hamburger", "sandwich"]])


if __name__ == "__main__":
	print vegetarian