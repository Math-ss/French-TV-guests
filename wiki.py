"""
Need :
-pickle
-request
-beautifulsoup

This programm parse the HTML code of Wikipedia to find the informations. 
It use part of the page called "Infobox". It's the table who show the main informations.
info.pck store all name of the guest but with misspelling, so we use the search page of Wikipédia 
to find the good link. All "print" are here to debug.

19/09/2019
By Mathgique
All right reserved(it's completly false but I have always dreamed to write that ;)
"""

import pickle as pck 
f = open("info.pck","rb")
allName = pck.load(f)

monde = dict()
poli = dict()
error = dict()
url = dict()
thelist = allName

import requests
from bs4 import BeautifulSoup

#The creation of a list of tests to find the job
test = [" Activité principale\n ", "Profession\n", "Activités", "Profession", "Activité", "Qualité", "Activité principale"]
testbis = dict()
testbis["Poste\n"] = "Sportif"
testbis["Position"] = "Sportif"
testbis["Nage\n"] = "Sportif"
testbis["Entraîneur\n"] = "Sportif"
testbis["Entraineur\n"] = "Sportif"
testbis["Prise de raquette\n"] = "Sportif"
testbis["Langue d’écriture "] = "Ecrivain"
testbis["Émissions\n"] = "Présentateur"
testbis[" Genre musical\n "] = "Chanteur"
testbis["Sport\n"] = "Sportif"

#This URL is the default results page of a search in Wikipédia(fr), without the word(s) we want search
sdebut = "https://fr.wikipedia.org/w/index.php?search="
sfin = "&title=Spécial%3ARecherche&profile=advanced&fulltext=1&advancedSearch-current=%7B\"namespaces\"%3A%5B0%5D%7D&ns0=1"
dec = 0

for name in thelist:
    
    print(dec)    
    
    #We add the word(s) to the search URL, it's the name of the guest
    surl = sdebut + name[0] + sfin
    print(name[0])
    
    #We parse the search URL's page, to find the first result(it's the page of the guest)
    req = requests.get(surl)
    soup = BeautifulSoup(req.text, "lxml")
    result = soup.find(name="ul", class_="mw-search-results")
    
    #If the guest has no Wiki-page
    if(result == None):
        print("We don't find the page!!!!\n")
        error[name[0]] = surl
        continue
    
    j = result.find(name="li")
    link = j.a
    
    surl = "https://fr.wikipedia.org" + link["href"] #The good URL !!
    b = link["href"].split("/")    
    url[name[0]] = b[2]
    print(surl)
    
    #We access the HTML file of the guest
    req = requests.get(surl)
    soup = BeautifulSoup(req.text, "lxml")
    aucun = True
    
    #We try to find the job by testing all word of the test lists
    monde[name[0]] = []    
    for y in test:
        part = soup.find_all(name="th", string=y)
        if(part != []):
            w = part[0]
            h = w.find_next(name="td")
            lname = h.find_all(name="a")
            aucun = False
            for c in lname:
                monde[name[0]].append(c.string)
    
    #If the guest is a politic man, we find his political party and we stock it in an other dictionnary
    part = soup.find_all(name="th", string="Parti politique\n")
    if(part != []):
        w = part[0]
        h = w.find_next(name="td")
        lname = h.find_all(name="a")
        aucun = False
        monde[name[0]].append("Politique")
        d =  dict()
        for c in lname:
            x = c.find_next(name="small")
            if(x != None):
                d[c.string] = x.string
        poli[name[0]] = d
                
            
    #We test some exceptions to determine his profession in particular cases
            
    for o in testbis.keys():
        if(soup.find_all(string=o) != []):
            aucun = False
            monde[name[0]].append(testbis[o])
        
    #If nothing works, we add to "error", the url of the guest's page
    if(aucun):
        error[name[0]] = surl
        print("ERROR!!!!!No words\n\n\n")
    dec = dec + 1



print(len(error))
     
allResults = dict()
allResults = {"url":url, "error":error, "politique":poli, "monde":monde}

#It miss the writing allResult in a Pickle

f.close()


