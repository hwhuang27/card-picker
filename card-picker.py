import sys, string, requests, urllib.request
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
from pprint import pprint
from bs4 import BeautifulSoup

class card_window(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.thumbnail = tk.PhotoImage(file="card.png")
		self.display = tk.Label(
			image=self.thumbnail, 
			bg="black"
			)
		self.display.pack(side="top")

		"""
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n(click me)"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack(side="top")
		"""
		self.quit = tk.Button(self, text="QUIT", fg="red",
		                      command=self.master.destroy)
		self.quit.pack(side="bottom")
		

class card_info():
	def __init__(self, soup):
		self.name = ""
		self.img_url = ""
		self.labels = np.chararray(7, itemsize=512, unicode=True)
		self.values = np.chararray(7, itemsize=512, unicode=True)
	
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

		if self.labels[0] == '':
			print('Card not found. Maybe check your spelling?')
			sys.exit(0)

		# extract card picture
		card_img = soup.find('img', class_="pi-image-thumbnail")
		self.img_url = str(card_img["src"])	
	
	# print functions for testing
	def print_labels(self):
		print(self.labels)

	def print_values(self):
		print(self.values)

	def print_imgurl(self):
		print(self.img_url)

def input_card_name():
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

	return card_name

def get_soup(name):
	URL = 'https://slay-the-spire.fandom.com/wiki/' + name
	page = requests.get(URL)
	return BeautifulSoup(page.content, 'lxml')

def main():
	card_name = input_card_name()	
	card_soup = get_soup(card_name)		# create soup object from StS wikia
	card = card_info(card_soup)			# create card object using scraped data
	urllib.request.urlretrieve(card.img_url, "card.png")	# download card thumbnail

	# ----- TkTinker GUI -----
	root = tk.Tk()
	root.title(card.name)
	root.configure(background="black")
	app = card_window(master=root)
	root.mainloop()

if __name__ == '__main__':
	main()