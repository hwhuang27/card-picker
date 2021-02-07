import sys
import numpy as np
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import tkinter as tk

class card_info():

	def __init__(self, soup):
		self.labels = np.empty(7, dtype='object')
		self.values = np.empty(7, dtype='object')

		# extract card labels from the HTML on the website
		card_labels = soup.find_all('h3', class_="pi-data-label pi-secondary-font")
		for index, label in enumerate(card_labels):
			self.labels[index] = str(label.text)
			print(self.labels[index])

		# extract corresponding card values
		card_data = soup.find_all('div', class_="pi-data-value pi-font")
		for index, value in enumerate(card_data):
			self.values[index] = str(value.text)
			print(self.values[index])

def main():
	card_name = input("Enter card name: ")
	if card_name == 'Strike':
		card_name = 'Strike_(Defect)'
	if card_name == 'Defend':
		card_name = 'Defend_(Defect)'

	URL = 'https://slay-the-spire.fandom.com/wiki/' + card_name
	page = requests.get(URL)
	card_soup = BeautifulSoup(page.content, 'lxml')

	card = card_info(card_soup)
	print(card.labels)
	print(card.values)




if __name__ == '__main__':
	main()