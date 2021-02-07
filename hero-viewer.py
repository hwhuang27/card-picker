import sys
import numpy as np
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import tkinter as tk

def main():
	# take card name and webscrape from the Slay the Spire wikia
	card_name = input("Enter card name: ")
	URL = 'https://slay-the-spire.fandom.com/wiki/' + card_name
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'lxml')
	
	info_arr = np.empty(7, dtype='object')
	data_arr = np.empty(7, dtype='object')

	card_info = soup.find_all('h3', class_="pi-data-label pi-secondary-font")
	for index, info in enumerate(card_info):
		info_arr[index] = str(info.text)
		print(info_arr[index])

	card_data = soup.find_all('div', class_="pi-data-value pi-font")
	for index, data in enumerate(card_data):
		data_arr[index] = str(data.text)
		print(data_arr[index])

	# create tkinter GUI
	window = tk.Tk()
	


if __name__ == '__main__':
	main()