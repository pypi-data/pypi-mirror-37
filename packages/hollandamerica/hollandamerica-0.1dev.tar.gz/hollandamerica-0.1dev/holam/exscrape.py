from bs4 import BeautifulSoup, Tag
import csv
from urllib.request import urlopen
import pandas as pd
from selenium import webdriver
import time
from langdetect import detect
import os

class exScrape(object):
	def __init__(self, lang, region):
		self.lang = lang
		self.region = region
		self.details = {}
	
	def excurScrape(self):
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
		
		url = "https://www.hollandamerica.com/"+self.lang+"/cruise-destinations/"+self.region+".excursions.html#sort=name%20asc&start=0&rows=12?"
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
			href = link.get_attribute("href")
			if href in list(details.keys()):
				href += "#"
			elif link.get_attribute("href") + "#" in list(details.keys()):
				href += "##"
			details[href] = {}
				
			if "en" in self.lang:
				details[href]["title"] = link.get_attribute("aria-label").replace("See Details ","")
			elif "es" in self.lang:
				details[href]["title"] = link.get_attribute("aria-label").replace("Ver detalles ","")
			elif "de" in self.lang:
				details[href]["title"] = link.get_attribute("aria-label").replace("Details ansehen ","")
			else:
				details[href]["title"] = link.get_attribute("aria-label").replace("Bekijk details ","")
			
			if "#" in href:
				details[href]["title"] += " (d)"
					
		
		for url in details:
			driver.get(url + "?")
			places = list(details.keys())
			
			heroimg = driver.find_elements_by_class_name("image-lazy-loader")
			details[url]["translated"] = "n"
			if len(heroimg) != 0:
				heroimg = driver.find_element_by_class_name("image-lazy-loader")
				
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
				elif str(heroimg.find_element_by_tag_name("img").get_attribute("src")).startswith("#.image") != -1:
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
				if "en" not in self.lang and len(desc[0].find_elements_by_tag_name("p")) != 0:
					text = desc[0].find_element_by_tag_name("p").get_attribute("innerText")
					if len(text) > 10:
						tlang = detect(text)
						if tlang in self.lang:
							details[url]["translated"] = "y"
						else:
							details[url]["translated"] = "n"
			else: 
				details[url]["description"] = "y"
				details[url]["translated"] = "n"
		
		if "en" in self.lang:
			if os.path.exists("en_US.txt"):
				os.remove("en_US.txt")
			with open("en_US.txt", "a") as enfile:
				enfile.write(str(details))
			with open(self.lang+".csv", "w", newline="") as csvfile:
				exwriter = csv.writer(csvfile)
				exwriter.writerow(["Hero Image", "Details", "Description", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["title"], str(key)])
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
		if os.path.exists(self.lang+".csv"):
			os.remove(self.lang+".csv")
		with open(self.lang+".csv", "w", newline="") as csvfile:
			exwriter = csv.writer(csvfile)
			if self.lang == "en_US":
				exwriter.writerow(["Hero Image", "Details", "Description", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["title"], str(key)])
			else:
				exwriter.writerow(["Hero Image", "Details", "Description", "in en search", "in en site", "translated", "name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["details"], details[key]["description"], details[key]["inengsearch"], details[key]["inen"], details[key]["translated"], details[key]["title"], str(key)])
			
		
		