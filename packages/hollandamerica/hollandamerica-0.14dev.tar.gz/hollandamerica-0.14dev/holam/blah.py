import csv
import urllib.request
import pandas as pd

def compare(fname1, fname2):
	with open(fname1) as csvfile:
		reader = pd.read_csv(fname1)
		data = reader['']
		print(data)