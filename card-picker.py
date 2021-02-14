import sys, string, requests, urllib.request
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
from pprint import pprint
from bs4 import BeautifulSoup

def input_card_name(card_name):
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

# creates card_info object with BeautifulSoup data
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

# main tkinter window
class query_window(tk.Frame):
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master, padx=15, pady=5)
		self.frame.pack()
		self.btmframe = tk.Frame(self.master)
		self.btmframe.pack(side='bottom', pady=10)
		self.make_query_field()
	    
	def make_query_field(self):
		# make logo display
		self.logo = tk.PhotoImage(file="logo.png")
		self.logo_disp = tk.Label(self.frame, image=self.logo)
		self.logo_disp.pack(side="top")	

		# create user input var / card name label
		self.user_input = tk.StringVar()
		self.name_label = tk.Label(self.frame, text="Card Name ")
		self.name_label.pack(side="left")

		# create text field
		self.query_box = tk.Entry(self.frame)
		self.query_box.pack(side="left")

		# create submit button
		self.submit_button = tk.Button(self.btmframe, text="Submit", command=lambda: self.submit())
		self.submit_button.pack()

	def submit(self):
		self.card_name = input_card_name(self.query_box.get())			# get query from text field
		self.card_soup = get_soup(self.card_name)						# create soup object from StS wikia
		self.card = card_info(self.card_soup)							# create card object using scraped data
		urllib.request.urlretrieve(self.card.img_url, "card.png")		# download card thumbnail
		self.open_card_window()

	# make a message box for query 
	def open_card_window(self):
		self.new_window = tk.Toplevel(self.master)
		self.new_card = card_window(self.new_window)

# new window to display card info 
class card_window(tk.Frame):
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_window)
		self.quitButton.pack()
		self.frame.pack()

	def close_window(self):
		self.master.destroy()	

def main():
	root = tk.Tk()
	root.title("StS-card-viewer")
	app = query_window(master=root)
	root.mainloop()

if __name__ == '__main__':
	main()