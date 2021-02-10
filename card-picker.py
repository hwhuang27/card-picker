import sys, string, requests, urllib.request
import numpy as np
import pandas as pd
import tkinter as tk
from pprint import pprint
from bs4 import BeautifulSoup

class card_info():
	def __init__(self, soup):
		self.name = ""
		self.labels = np.chararray(7, itemsize=512, unicode=True)
		self.values = np.chararray(7, itemsize=512, unicode=True)
		self.img_url = ""

		# extract card title
		card_title = soup.find(id="firstHeading").text
		self.name = str(card_title)

		# extract card labels from the HTML on the website
		card_labels = soup.find_all('h3', class_="pi-data-label pi-secondary-font")
		for index, label in enumerate(card_labels):
			self.labels[index] = str(label.text)

		# extract corresponding card values
		card_data = soup.find_all('div', class_="pi-data-value pi-font")
		for index, value in enumerate(card_data):
			self.values[index] = str(value.text)

		# extract card picture
		card_img = soup.find('img', class_="pi-image-thumbnail")
		self.img_url = str(card_img["src"])

	def print_labels(self):
		print(self.labels)

	def print_values(self):
		print(self.values)

	def print_imgurl(self):
		print(self.img_url)

def main():
	card_name = input("Enter card name: ")

	# capitalize if not already and handle special cases
	if "'" in card_name:
		card_name = card_name.replace("'", "%27")
	card_name = string.capwords(card_name)
	if " " in card_name:
		card_name = card_name.replace(" ", "_")

	# strike/defend defaults to class: defect 
	if card_name == 'Strike':
		card_name = 'Strike_(Defect)'
	if card_name == 'Defend':
		card_name = 'Defend_(Defect)'

	URL = 'https://slay-the-spire.fandom.com/wiki/' + card_name
	page = requests.get(URL)
	card_soup = BeautifulSoup(page.content, 'lxml')

	card = card_info(card_soup)
	if card.labels[0] == '':
		print('Card not found. Maybe check your spelling?')
		sys.exit(0)
	
	card.print_labels()
	card.print_values()
	card.print_imgurl()

	urllib.request.urlretrieve(card.img_url, "card.png")


if __name__ == '__main__':
	main()