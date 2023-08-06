import re

def numextract(filename):
	numbers = []
	try:
		for data in open(filename):   
			lines = data.split(" ")
			for words in lines:
				numbers.append(re.findall('[\d]+',words))
		numlist = [j for i in numbers for j in i]
		return numlist
	except:
		print("File not found !")