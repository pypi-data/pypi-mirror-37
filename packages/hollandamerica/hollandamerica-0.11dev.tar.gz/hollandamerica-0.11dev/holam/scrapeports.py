from bs4 import BeautifulSoup, Tag
import csv
import urllib.request
import pandas as pd
from selenium import webdriver
import time

class Reader(object):
	def __init__(self, filename):
		self.filename = filename
		
	def portscrape(self, pnames, langarg):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_argument('--ignore-ssl-errors')
		driver = webdriver.Chrome(options=options)
		print(pnames)
		for i in range(0, len(pnames)):
			pnames[i] = pnames[i].lower()
			if pnames[i].endswith(" "):
				pnames[i] = pnames[i].rstrip()
			pnames[i] = pnames[i].replace("(", "")
			pnames[i] = pnames[i].replace(")", "")
			pnames[i] = pnames[i].replace(" ", "-")
			pnames[i] = pnames[i].replace(",", "")
		print(pnames)
	

		driver.get("https://www.hollandamerica.com/")
		time.sleep(1)
		urls = []
		info = {}
		if langarg == "de":
			dropdown = driver.find_element_by_class_name('dropdown-label')
			dropdown.click()
			items = driver.find_elements_by_class_name('dropdown-item')
			for item in items:
				if '-3' in str(item):
					item.click()
					for name in pnames:
						info[name] = {}
						url = "http://www.hollandamerica.com/de_DE/ports/"+name+".html?"
						info[name]["uri"] = url
						driver.get(url)
						img = ""
						src = ""
						if len(driver.find_elements_by_class_name('image-lazy-loader')) != 0:
							image = driver.find_element_by_class_name('image-lazy-loader')
							if len(image.find_elements_by_tag_name("img")) != 0:
								img = image.find_element_by_tag_name("img")
								print(img)
								src = img.get_attribute("src")
								if '00003242' not in src and ('.jpg' in src.lower() or '.png' in src.lower()):
									info[name]["heropresent"] = "y"
								else:
									info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = src
							
							else:
								info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = "n"
						else:
							info[name]["heropresent"] = "dne"
							info[name]["imgsrc"] = "n"
						if len(driver.find_elements_by_class_name('desc')) != 0:
							desc = driver.find_element_by_class_name('desc')
							if len(desc.find_elements_by_tag_name("p")) != 0:
								info[name]["textpresent"] = "y"
							else:
								info[name]["textpresent"] = "n"
						else:
							info[name]["textpresent"] = "dne"
						
						if len(driver.find_elements_by_class_name('afar-text')) != 0:
							afar = driver.find_element_by_class_name('afar-text')
							if len(afar.find_elements_by_tag_name("span")) != 0:
								info[name]["404"] = "n"
							else:
								info[name]["404"] = "y"
						else:
							info[name]["404"] = "y"
						
		elif langarg == "en":
			for name in pnames:
				info[name] = {}
				url = "http://www.hollandamerica.com/en_US/ports/"+name+".html?"
				info[name]["uri"] = url
				driver.get(url)
				img = ""
				src = ""
				if len(driver.find_elements_by_class_name('image-lazy-loader')) != 0:
					image = driver.find_element_by_class_name('image-lazy-loader')
					if len(image.find_elements_by_tag_name("img")) != 0:
						img = image.find_element_by_tag_name("img")
						print(img)
						src = str(img.get_attribute("src"))
						if '00003242' not in src and ('.jpg' in src.lower() or '.png' in src.lower()):
							info[name]["heropresent"] = "y"
						else:
							info[name]["heropresent"] = "n"
						info[name]["imgsrc"] = src
					
					else:
						info[name]["heropresent"] = "n"
						info[name]["imgsrc"] = "n"
				else:
					info[name]["heropresent"] = "dne"
					info[name]["imgsrc"] = "n"
				if len(driver.find_elements_by_class_name('desc')) != 0:
					desc = driver.find_element_by_class_name('desc')
					if len(desc.find_elements_by_tag_name("p")) != 0:
						info[name]["textpresent"] = "y"
					else:
						info[name]["textpresent"] = "n"
				else:
					info[name]["textpresent"] = "dne"
				
				if len(driver.find_elements_by_class_name('afar-text')) != 0:
					afar = driver.find_element_by_class_name('afar-text')
					if len(afar.find_elements_by_tag_name("span")) != 0:
						info[name]["404"] = "n"
					else:
						info[name]["404"] = "y"
				else:
					info[name]["404"] = "y"
						
		elif langarg == "es":
			dropdown = driver.find_element_by_class_name('dropdown-label')
			dropdown.click()
			items = driver.find_elements_by_class_name('dropdown-item')
			for item in items:
				if '-4' in str(item):
					item.click()
					for name in pnames:
						info[name] = {}
						url = "http://www.hollandamerica.com/es_ES/ports/"+name+".html?"
						info[name]["uri"] = url
						driver.get(url)
						img = ""
						src = ""
						if len(driver.find_elements_by_class_name('image-lazy-loader')) != 0:
							image = driver.find_element_by_class_name('image-lazy-loader')
							if len(image.find_elements_by_tag_name("img")) != 0:
								img = image.find_element_by_tag_name("img")
								print(img)
								src = img.get_attribute("src")
								if '00003242' not in src and ('.jpg' in src.lower() or '.png' in src.lower()):
									info[name]["heropresent"] = "y"
								else:
									info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = src
							
							else:
								info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = "n"
						else:
							info[name]["heropresent"] = "dne"
							info[name]["imgsrc"] = "n"
						if len(driver.find_elements_by_class_name('desc')) != 0:
							desc = driver.find_element_by_class_name('desc')
							if len(desc.find_elements_by_tag_name("p")) != 0:
								info[name]["textpresent"] = "y"
							else:
								info[name]["textpresent"] = "n"
						else:
							info[name]["textpresent"] = "dne"
						
						if len(driver.find_elements_by_class_name('afar-text')) != 0:
							afar = driver.find_element_by_class_name('afar-text')
							if len(afar.find_elements_by_tag_name("span")) != 0:
								info[name]["404"] = "n"
							else:
								info[name]["404"] = "y"
						else:
							info[name]["404"] = "y"
						
		elif langarg == "nl":
			dropdown = driver.find_element_by_class_name('dropdown-label')
			dropdown.click()
			items = driver.find_elements_by_class_name('dropdown-item')
			for item in items:
				if '-5' in str(item):
					item.click()
					for name in pnames:
						info[name] = {}
						url = "http://www.hollandamerica.com/nl_NL/ports/"+name+".html?"
						info[name]["uri"] = url
						driver.get(url)
						img = ""
						src = ""
						if len(driver.find_elements_by_class_name('image-lazy-loader')) != 0:
							image = driver.find_element_by_class_name('image-lazy-loader')
							if len(image.find_elements_by_tag_name("img")) != 0:
								img = image.find_element_by_tag_name("img")
								print(img)
								src = str(img.get_attribute("src"))
								if '00003242' not in src and ('.jpg' in src.lower() or '.png' in src.lower()):
									info[name]["heropresent"] = "y"
								else:
									info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = src
							
							else:
								info[name]["heropresent"] = "n"
								info[name]["imgsrc"] = "n"
						else:
							info[name]["heropresent"] = "dne"
							info[name]["imgsrc"] = "n"
						if len(driver.find_elements_by_class_name('desc')) != 0:
							desc = driver.find_element_by_class_name('desc')
							if len(desc.find_elements_by_tag_name("p")) != 0:
								info[name]["textpresent"] = "y"
							else:
								info[name]["textpresent"] = "n"
						else:
							info[name]["textpresent"] = "dne"
						
						if len(driver.find_elements_by_class_name('afar-text')) != 0:
							afar = driver.find_element_by_class_name('afar-text')
							if len(afar.find_elements_by_tag_name("span")) != 0:
								info[name]["404"] = "n"
							else:
								info[name]["404"] = "y"
						else:
							info[name]["404"] = "y"
						
						
		if langarg == "de":
			with open('de.csv', 'w', newline='') as csvfile:
				portwriter = csv.writer(csvfile)
				portwriter.writerow(['de', 'url', '404', 'hero', 'filename', 'text'])
				for key in info:
					portwriter.writerow([key, info[key]["uri"], info[key]["404"], info[key]["heropresent"], info[key]["imgsrc"], info[key]["textpresent"]])
		elif langarg == "nl":
			with open('nl.csv', 'w', newline='') as csvfile:
				portwriter = csv.writer(csvfile)
				portwriter.writerow(['nl', 'url', '404', 'hero', 'filename', 'text'])
				for key in info:
					portwriter.writerow([key, info[key]["uri"], info[key]["404"], info[key]["heropresent"], info[key]["imgsrc"], info[key]["textpresent"]])
		elif langarg == "es":
			with open('es.csv', 'w', newline='') as csvfile:
				portwriter = csv.writer(csvfile)
				portwriter.writerow(['es', 'url', '404', 'hero', 'filename', 'text'])
				for key in info:
					portwriter.writerow([key, info[key]["uri"], info[key]["404"], info[key]["heropresent"], info[key]["imgsrc"], info[key]["textpresent"]])
		elif langarg == "en":
			with open('en.csv', 'w', newline='') as csvfile:
				portwriter = csv.writer(csvfile)
				portwriter.writerow(['en', 'url', '404', 'hero', 'filename', 'text'])
				for key in info:
					portwriter.writerow([key, info[key]["uri"], info[key]["404"], info[key]["heropresent"], info[key]["imgsrc"], info[key]["textpresent"]])
	
		with open("new.txt", "a") as f:
			f.write(str(info))
		
			


	def read(self):
		with open(self.filename) as csvfile:
			reader = pd.read_csv(self.filename)
			firstcol = reader['pname']
			print(firstcol)
			items = []
			for item in firstcol:
				items.append(item)
			self.visit(items, "en")
