from lxml import html
import requests
import sys #can be removed when storing directly to database
import os # can also be removed
from constants import eventFields

def EventObj(*argv):

	def __init__(self,)



def htmlTree( URL ):
    page = requests.get(URL)
    websitetree = html.fromstring(page.content)
    return websitetree

def Scraper(websitetree, xpaths):

	attributes = []

	for xpath in xpaths:
		attributes.append(websitetree.xpath(xpath))

	for i in range(len(attributes[0])):



def Scraper (websitetree, xpaths):

	#Extracts lists of attributes from webpage by using the xpath websitetree

    # This will extract a list of shoe names on page
    shoeName_codeName = (websitetree.xpath(xpaths[0]))
    # This will extract list of exact urls
    shoeURL = (websitetree.xpath(xpaths[1]))
    # This will extract a list of shoe prices
    lowestprice = (websitetree.xpath(xpaths[2]))
    #This will extract a list of images
    imgURL =  (websitetree.xpath(xpaths[3]))

    for x in range (len(shoeName_codeName)): #iterate through all shoe listings on page
        if shoeURL[x] in allShoes.keys(): #if value is not unique to keys exclude
            continue
        else:
            try:

                print ("Storing New Shoe", "NAME:", shoeName_codeName[x].strip(), "PRICE:", lowestprice[x], '\n')
                allShoes[shoeURL[x]] = (ShoeObj(shoeName_codeName[x].strip(), lowestprice[x], shoeURL[x], imgURL[x]))

                orig_sys = sys.stdout #saving output stream

                ##
                shoelist = open('shoelist.txt', 'a')
                sys.stdout = shoelist #redirecting output to output file shoelist.txt
                allShoes[shoeURL[x]].shoelist()
                ##
                namelist = open('namelist.txt', 'a')
                sys.stdout = namelist #redirecting output to output file namelist.txt
                allShoes[shoeURL[x]].namelist()
                ##

                sys.stdout = orig_sys

            except IndexError:
                print("OUT OF RANGE ITEM")
