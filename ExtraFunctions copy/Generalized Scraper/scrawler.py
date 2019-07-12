################## FLIGHTCLUB SCRAWLER ######################

## IMPORTS ##

from lxml import html
import requests
import sys #can be removed when storing directly to database
import os # can also be removed

allShoes = {}

########################################## FUNCTIONS ####################################################################

# parse html request and get get tree structure for xpath searching
def htmlTree( URL ):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    return tree

##def getSizes(shoe):
##	tree = htmlTree(shoe.URL)
##    shoe.sizes = (tree.xpath(sizexpath))

##def getPrice(shoe):
##		pricexpath = ""
##		for size in shoe.sizes:
##		tree = htmlTree(shoe.URL)
##		for sizes in shoe.sizes
##       pricexpath = tree.getpath(r)  #make sure to only return value that exactly matches string #test amout of values returned
##		shoe.price.append(tree.xpath(pricexpath)) #test the correctness of the returned value

# Scrape Given URL to extract fields
def Scraper (tree, xpaths):
    # This will extract a list of shoe names on page
    shoeName_codeName = (tree.xpath(xpaths[0]))
    # This will extract list of exact urls
    shoeURL = (tree.xpath(xpaths[1]))
    # This will extract a list of shoe prices
    lowestprice = (tree.xpath(xpaths[2]))
    #This will extract a list of images
    imgURL =  (tree.xpath(xpaths[3]))

    for x in range (0,len(shoeName_codeName)): #iterate through all shoe listings on page
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

#Iteratively search through given list of html shoe directories *seed urls* and pass url to scraper
def Crawler ( Robj ):
    for seed in Robj.seeds: #seed urls declared in retailer class
        pnum=1
        while( True ): #will continute until the break function inside the function is triggered
            try:
                url = seed + '?' + Robj.urlflgs[0] +  '=' + str(pnum) + '&' + Robj.urlflgs[2]
            except IndexError:
                print ("No Limit Flag")
                url = seed + '?' + Robj.urlflgs[0] +  '=' + str(pnum)

            print ("Scraping Site: " , url)
            tree = htmlTree (url)
            Scraper(tree, Robj.xpaths) #scrapes each page on the fly
            #print ('Does:' , tree.xpath(Robj.xpaths[4])[0].strip() ,'equal' , Robj.urlflgs[1]) #// used for testing nxval validity
            # this searches the html page for the "next" element which varies page to page, var specific to page stored in Robj.nxval
            if (pnum == 1):
                if (tree.xpath(Robj.xpaths[4])[0].strip() != Robj.urlflgs[1] ): #Very Important IF STATEMENT if its the first page there is no prev so next text in first position
                    break														#Femi: Previous line give me an out of range error, like one of the numbers in the IF statement 																#is not an actual index in the list
            else:
                try:
                    if (tree.xpath(Robj.xpaths[4])[0].strip() != Robj.urlflgs[1] ): # Every other page should have a nxval in the second position, after previous val second position
                        break
                except IndexError: # On last page there is a previous button but no next button so this is the last page
                    break
            pnum += 1
################################# CLASSES ##################################################################

class ShoeObj:
    def __init__(self, name, lprice, URL, imgURL):
        self.name = name.replace('"', '*') #make optional
        self.lprice = lprice #make optional
        self.URL = URL
        self.imgURL = imgURL
        self.sizes = []
        self.multSZ = False;
        self.prices= []

    def namelist (self):
        print ('\"' +self.name +'\",') ##.replace('*', '') #Print out shoelist names

    def shoelist (self):
        print ('"' ,self.name, '|', self.lprice ,'|' , self.URL ,'|' , self.sizes , '|' ,self.imgURL,'",') #Print out full shoe information


class RetailerObj:
        def __init__(self, seedurls, xpathvars, urlflags): #change nextpgxpath to go into the object, change flags to take pgincn nxval and extras
            self.seeds = seedurls       # Www.example.com
            self.xpaths = xpathvars     # name,url,price,image
            self.urlflgs = urlflags     # flags : PageID, NextID, ExtraFlgs

#################################### FUNCTIONS ##################################################################
if __name__ == "__main__":

    try:
        os.remove("shoelist.txt")
        os.remove("namelist.txt")
    except FileNotFoundError:
        pass

    Retailers = [] #this will contain all retailer objects

    consts = open ('Constants.txt','r') #open retailers list

    lists = [[] for i in range(0, 3)] #create three lists within a list
    a=0
    rcount=0 #count of all retailers

    for line in consts:
        if line[0] == '$':
            rcount=rcount+1
            a = 0 #reset list reference
            print ("Adding a retailer ", rcount ,"to list " )
            Retailers.append(RetailerObj(lists[0],lists[1],lists[2])) # retailer object instantiation
            lists[0] =[]; lists[1]=[]; lists[2]=[]
            continue
        if line[0] == ' ' or line[0] == '#' or line[0] == '\n':
            continue
        if line[0] != '&':
            lists[a].append(line[:-1])
        else:
            a=a+1
        if line[0] == '!':
            break

    consts.close() #close list of retailers

    for retailer in Retailers:
        Crawler(retailer)
