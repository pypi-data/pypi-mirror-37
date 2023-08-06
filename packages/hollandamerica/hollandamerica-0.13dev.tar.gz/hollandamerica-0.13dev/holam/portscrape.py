from bs4 import BeautifulSoup, Tag
import csv
from urllib.request import urlopen
import pandas as pd
from selenium import webdriver
import time
from langdetect import detect
import os

class portScrape(object):
	def __init__(self, lang, region):
		self.lang = lang
		self.region = region
		self.details = {}
	
	def portscrape(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_argument('--ignore-ssl-errors')
		driver = webdriver.Chrome(options=options)
		details = {}
		driver.get("https://www.hollandamerica.com")
		dropdown = driver.find_element_by_class_name('dropdown-label')
		dropdown.click()
		items = driver.find_elements_by_class_name('dropdown-item')
		if "de" in self.lang:
			for item in items:
				if '-3' in str(item):
					item.click()
		elif "es" in self.lang:
			for item in items:
				if '-4' in str(item):
					item.click()
		elif "nl" in self.lang:
			for item in items:
				if '-5' in str(item):
					item.click()
		
		url = "https://www.hollandamerica.com/"+self.lang+"/cruise-destinations/"+self.region+".ports.html#sort=name%20asc&start=0&rows=12?"
		driver.get(url)
		page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
		pages = int(driver.find_element_by_class_name("total-pages").get_attribute("innerText"))
		
		print(pages)
		next = driver.find_elements_by_class_name("next")
		x = True
		while x == True:
			if page < (pages-1):
				page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
				time.sleep(2)
				print(next)
				tiles = driver.find_elements_by_class_name("port-detail-tile")
				for tile in tiles:
					link = tile.find_element_by_tag_name("a")
					if link.get_attribute("href") in list(details.keys()):
						details[(link.get_attribute("href")) + "#"] = {}
						details[(link.get_attribute("href")) + "#"]["title"] = link.get_attribute("title") + " (d)"
					else:	
						details[(link.get_attribute("href"))] = {}
						details[(link.get_attribute("href"))]["title"] = link.get_attribute("title")
						
				page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
				if page < pages:
					next[0].click()
				else:
					x = False
			else:
				x = False
		
		time.sleep(1)
		page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
		next = driver.find_elements_by_class_name("next")
		print(next)
		links = driver.find_elements_by_class_name("see-details-cta-label")
		for link in links:
			if link.get_attribute("href") in list(details.keys()):
				details[(link.get_attribute("href")) + "#"] = {}
				if "en" in self.lang:
					details[(link.get_attribute("href")) + "#"]["title"] = link.get_attribute("aria-label").replace("See Details ","") + " (d)"
				elif "es" in self.lang:
					details[(link.get_attribute("href")) + "#"]["title"] = link.get_attribute("aria-label").replace("Ver detalles ","") + " (d)"
				elif "de" in self.lang:
					details[(link.get_attribute("href")) + "#"]["title"] = link.get_attribute("aria-label").replace("Details ansehen ","") + " (d)"
				else:
					details[(link.get_attribute("href")) + "#"]["title"] = link.get_attribute("aria-label").replace("Bekijk details ","") + " (d)"
			else:	
				details[(link.get_attribute("href"))] = {}
				if "en" in self.lang:
					details[(link.get_attribute("href"))]["title"] = link.get_attribute("aria-label").replace("See Details ","")
				elif "es" in self.lang:
					details[(link.get_attribute("href"))]["title"] = link.get_attribute("aria-label").replace("Ver detalles ","")
				elif "de" in self.lang:
					details[(link.get_attribute("href"))]["title"] = link.get_attribute("aria-label").replace("Details ansehen ","")
				else:
					details[(link.get_attribute("href"))]["title"] = link.get_attribute("aria-label").replace("Bekijk details ","")
			
					
		
		for url in details:
			driver.get(url + "?")
			places = list(details.keys())
			
			heroimg = driver.find_elements_by_class_name("image-lazy-loader")
			details[url]["translated"] = "n"
			if len(heroimg) != 0:
				heroimg = driver.find_element_by_class_name("image-lazy-loader")
				details[url]["imgsrc"] = heroimg.find_element_by_tag_name("img").get_attribute("src")
				if str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("sunset-water") != -1:
					details[url]["hero image"] = "y (placeholder)"
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("ship-quarter--10") != -1: 
					details[url]["hero image"] = "y (placeholder)"
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("ship-side--10") != -1:
					details[url]["hero image"] = "y (placeholder)"
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("ship-front--10") != -1:
					details[url]["hero image"] = "y (placeholder)"
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("water--10") != -1:
					details[url]["hero image"] = "y (placeholder)"
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).find("#.image") != -1:
					details[url]["hero image"] = "y (placeholder)"
				else:
					details[url]["hero image"] = "n"
			else:
				details[url]["hero image"] = "y"
			
			facts = driver.find_elements_by_class_name("shorex-key-facts")
			if len(facts) != 0:
				details[url]["details"] = "n"
			else: 
				details[url]["details"] = "y"
				
			desc = driver.find_elements_by_class_name("desc")
			if len(desc) != 0:
				details[url]["description"] = "n"
				if "en" not in self.lang and len(desc) != 0:
					if len(desc[0].find_elements_by_tag_name("p")) != 0:
						text = desc[0].find_element_by_tag_name("p").get_attribute("innerText")
						details[url]["shortdesctext"] = text
						details[url]["longdesctext"] = text
						
						details[url]["translated"] = "n"
						if len(text) > 10:
							tlang = detect(text)
							if tlang in self.lang:
								details[url]["translated"] = "y"
							else:
								details[url]["translated"] = "n"
						if "coming soon" in desc[0].find_element_by_tag_name("p").get_attribute("innerText"):
							details[url]["description"] = "needscopy"
					else:
						details[url]["shortdesctext"] = desc[0].get_attribute("innerText")
						details[url]["longdesctext"] = desc[0].get_attribute("innerText")
				else:
					details[url]["desctext"] = desc[0].get_attribute("innerText")
					tlang = detect(details[url]["desctext"])
					buttons = driver.find_elements_by_class_name("readmoreLink")
					if len(buttons) != 0:
						button = driver.find_element_by_class_name("readmoreLink")
						readmore = button.find_element_by_tag_name("a")
						readmore.click()
						newtext = desc[0].find_elements_by_tag_name("p")
						details[url]["longdesctext"] = ""
						for item in newtext:
							newthing = item.get_attribute("innerText")
							details[url]["longdesctext"] += newthing
						if tlang in self.lang:
							details[url]["translated"] = "y"
						else:
							details[url]["translated"] = "n"
						details[url]["description"] = "n"
					else:
						details[url]["longdesctext"] = ""
			else: 
				details[url]["desctext"] = "???"
				details[url]["description"] = "y"
				details[url]["translated"] = "n"
		
		if "en" in self.lang:
			if os.path.exists("en_US.txt"):
				os.remove("en_US.txt")
			with open("en_US.txt", "a") as enfile:
				enfile.write(str(details))
			with open(self.lang+""+".csv", "w", newline="") as csvfile:
				exwriter = csv.writer(csvfile)
				exwriter.writerow(["Hero Image", "imgsrc", "Details", "Description", "desctext", "longtext", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["imgsrc"], details[key]["details"], details[key]["description"], str(details[key]["desctext"]), str(details[key]["longdesctext"]), details[key]["title"], str(key)])
		else:
			data = ""
			with open('en_US.txt', 'r') as newfile:
				data = newfile.read().replace('\n', '').replace("en_US", self.lang)
				print(data)
			for url in details:
				string = url
				print(string)
				if string in data:
					details[url]["inengsearch"] = "y"
				else:
					details[url]["inengsearch"] = "n"
				enstring = string.replace(self.lang, "en_US")
				html = urlopen(enstring)
				if html.getcode() == "404":
					details[url]["inen"] = "n"
				else:
					details[url]["inen"] = "y"
				
		print(details)
		if os.path.exists(self.lang+""+self.region+".csv"):
			os.remove(self.lang+""+self.region+".csv")
		with open(self.lang+""+self.region+".csv", "w", newline="") as csvfile:
			exwriter = csv.writer(csvfile)
			if self.lang == "en_US":
				exwriter.writerow(["Hero Image", "imgsrc", "Details", "Description", "desctext", "longtext", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["imgsrc"], details[key]["details"], details[key]["description"], details[key]["desctext"], details[key]["longdesctext"], details[key]["title"], str(key)])
			else:
				exwriter.writerow(["Hero Image", "Details", "Description", "in en search", "in en site", "translated", "name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], str(details[key]["shortdesctext"]), details[key]["inengsearch"], details[key]["inen"], details[key]["translated"], details[key]["title"], str(key)])
			
		
		