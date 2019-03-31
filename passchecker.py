import os
import sys
import re
import subprocess
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def run(cmd):
	return subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)

def get_profiles():

	get_profiles_name = "netsh wlan show profiles"
	get_profile_pass = 'netsh wlan show profile name="{}" key=clear'

	output = run(get_profiles_name) # Exécute la commande get_profiles_name_cmd

	results = re.findall(r"(\?)?: (?P<name>.*)", output.stdout.read()) # Récupération du nom des profiles dans output.stdout

	Profiles = [] #Liste des profiles Nom + Mot de passe

	max_ = None

	for i, result in enumerate(results):
		profile_name = result[1]

		if profile_name != '':
			output = run(get_profile_pass.format(profile_name)) # Exécution de la commande get_profile_pass

			lines = output.stdout.readlines() 

			key_line = lines[-11:-10][0] # Extraction de la ligne du mot de passe

			key = re.search(r": (?P<pass>.*)",key_line) # Extraction du mot de passe

			Profiles.append((profile_name,key.group('pass'))) # Ajout du couple (nom,mot de passe) à la liste des profiles
			
			if max_ and i >= max_:
				break

	return Profiles


class Win(Tk): 
	def __init__(self):
		super().__init__()
		self.title("Mointi PassChecker")
		self.container = Frame(self)
		self.table = ttk.Treeview(self.container, columns=('name','pass'))
		self.current_name = StringVar()
		self.current_pass = StringVar()

		self.initUI()
		self.update()
		self.bluild_content()

	def initUI(self):
		table = self.table
		container = self.container

		img_wifi = Image.open("icons/wifi.png")
		img_key = Image.open("icons/key.png")
		self.wifi = ImageTk.PhotoImage(img_wifi)
		self.key = ImageTk.PhotoImage(img_key)

		# Colonnes
		table.column("#0", width=60, stretch=NO)
		table.heading('#0', text='n°')
		table.heading('name', text='Nom du profil',image=self.wifi)
		table.heading('pass', text='Mot de passe', image=self.key)

		#TConfiguration des tags
		table.tag_configure("bg1", background="#E8E8E8")
		table.tag_configure("bg2", background="#fff")
		table.tag_bind('item', '<ButtonRelease-1>', self.selectItem)

		vsb = ttk.Scrollbar(container,orient="vertical",command=self.table.yview)
		self.table.configure(yscrollcommand=vsb.set)

		#Footer
		Footer = Frame(self, height=30, highlightbackground="gray",  highlightthickness=1, padx=10, pady=10)

		profile_label = Label(Footer, text="Nom du profil:")
		pass_label = Label(Footer, text="Mot de passe:")
		profile_entry = ttk.Entry(Footer,textvariable=self.current_name)
		pass_entry = ttk.Entry(Footer,textvariable=self.current_pass)

		#Placement
		container.pack(side=TOP, fill=BOTH, expand=1) 
		table.pack(side=LEFT, fill=BOTH, expand=1)
		vsb.pack(side=RIGHT, fill=Y)
		Footer.pack(side=BOTTOM, fill=X)

		profile_label.grid(row=0, column=0, sticky=W)
		profile_entry.grid(row=1, column=0, padx=5)
		pass_label.grid(row=0, column=1, sticky=W)
		pass_entry.grid(row=1, column=1)


	def selectItem(self,e):
	    curItem = self.table.focus()
	    val = self.table.item(curItem)['values']
	    self.current_name.set(val[0])
	    self.current_pass.set(val[1])


	def bluild_content(self):
		for i, profile in enumerate(get_profiles()):
			tag = "bg1"
			name = profile[0]
			pass_ = profile[1]

			if i % 2 :
				tag = "bg2"
			if pass_ == '1':
				pass_ = "Aucun"

			self.table.insert('', 'end', text=str(i+1), values=(name,pass_), tags=('item',tag))


def main():
	app = Win()
	app.mainloop()

if __name__ == "__main__":
	main()