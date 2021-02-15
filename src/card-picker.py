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
		self.frame = tk.Frame(self.master)
		self.frame.pack(padx=20, pady=10)
		self.btmframe = tk.Frame(self.master)
		self.btmframe.pack(side='bottom', pady=10)
		self.make_query_field()
	    
	def make_query_field(self):
		self.logo = tk.PhotoImage(file="../img/logo.png")
		self.logo_disp = tk.Label(self.frame, image=self.logo)
		self.logo_disp.pack(side="top")	

		self.user_input = tk.StringVar()
		self.name_label = tk.Label(self.frame, text="Card Name ", font=("Ubuntu", 12))
		self.name_label.pack(side="left")

		self.query_box = tk.Entry(self.frame)
		self.query_box.pack(side="left")

		self.submit_button = tk.Button(self.btmframe, text="Submit", font=("Ubuntu", 13, "bold"),
			command=lambda: self.submit())
		self.submit_button.pack()

	def submit(self):
		self.card_name = input_card_name(self.query_box.get())				# get query from text field
		self.card_soup = get_soup(self.card_name)							# create soup object from StS wikia
		self.card = card_info(self.card_soup)								# create card object using scraped data
		urllib.request.urlretrieve(self.card.img_url, "../img/card.png")	# download card thumbnail
		self.open_card_window()

	# make a message box for query 
	def open_card_window(self):
		self.new_window = tk.Toplevel(self.master)
		self.new_card = card_window(self.new_window, self.card)

# new window to display card info 
class card_window(tk.Frame):
	def __init__(self, master, card):
		self.master = master
		self.master.title(card.name)
		self.frame = tk.Frame(self.master, padx=10, pady=5)
		self.frame.pack()
		self.btmframe = tk.Frame(self.master)
		self.btmframe.pack(side='bottom', pady=5)
		self.make_thumbnail()
		self.make_card_fields(card)
		self.make_quit_button()

	def make_thumbnail(self):
		self.thumbnail = tk.PhotoImage(file="../img/card.png")
		self.thumb_disp = tk.Label(self.frame, image=self.thumbnail)
		self.thumb_disp.pack(side="top")

	def make_quit_button(self):
		self.quit_button = tk.Button(self.btmframe, text='Close', width=25, 
			font=("Ubuntu", 13, "bold"), command=self.close_window)
		self.quit_button.pack()

	def make_card_fields(self, card):
		self.class_label = tk.Label(self.frame, text=card.labels[0], font=("Ubuntu Mono", 14, "bold"))
		self.class_label.pack()
		self.class_value = tk.Label(self.frame, text=card.values[0], font=("Ubuntu Mono", 12))
		self.class_value.pack(pady=5)

		self.type_label = tk.Label(self.frame, text=card.labels[1], font=("Ubuntu Mono", 14, "bold"))
		self.type_label.pack()
		self.type_value = tk.Label(self.frame, text=card.values[1], font=("Ubuntu Mono", 12))
		self.type_value.pack(pady=5)

		self.rarity_label = tk.Label(self.frame, text=card.labels[2], font=("Ubuntu Mono", 14, "bold"))
		self.rarity_label.pack()
		self.rarity_value = tk.Label(self.frame, text=card.values[2], font=("Ubuntu Mono", 12))
		self.rarity_value.pack(pady=5)

		if card.values[5] == '':
			self.cost_label = tk.Label(self.frame, text=card.labels[3], font=("Ubuntu Mono", 14, "bold"))
			self.cost_label.pack()
			self.cost_value = tk.Label(self.frame, text=card.values[3], font=("Ubuntu Mono", 12))
			self.cost_value.pack(pady=5)
		else:
			self.cost_label = tk.Label(self.frame, text=card.labels[3] + " (" + card.labels[5] + ")",
				font=("Ubuntu Mono", 14, "bold"))
			self.cost_label.pack()
			self.cost_value = tk.Label(self.frame, text=card.values[3] + " (" + card.values[5] + ")",
				font=("Ubuntu Mono", 12))
			self.cost_value.pack(pady=5)
		
		self.effect_label = tk.Label(self.frame, text=card.labels[4], font=("Ubuntu Mono", 14, "bold"))
		self.effect_label.pack()
		self.effect_value = tk.Label(self.frame, text=card.values[4], font=("Ubuntu Mono", 12), wraplength=300)
		self.effect_value.pack(pady=3)

		if card.values[6] != '':
			self.effect2_label = tk.Label(self.frame, text=card.labels[6], font=("Ubuntu Mono", 14, "bold"))
			self.effect2_label.pack()
			self.effect2_value = tk.Label(self.frame, text=card.values[6], font=("Ubuntu Mono", 12), wraplength=300)
			self.effect2_value.pack(pady=3)		

	def close_window(self):
		self.master.destroy()	

def main():
	root = tk.Tk()
	root.title("Card Viewer")
	root.iconphoto(True, tk.PhotoImage(file="../img/icon.png"))
	app = query_window(master=root)
	root.mainloop()

if __name__ == '__main__':
	main()

# --- to do ---

# event handlers for enterkey-submit, esc-close, etc. for both windows
# fix grammatical issues for labels/values
# make program not exit on typo