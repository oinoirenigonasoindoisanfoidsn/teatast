import urllib.request as urllib
from bs4 import BeautifulSoup
import numpy 
import re
import sys
import os
#import subprocess
import webbrowser

# --------------------------------------------------------------------------------------
# Get the HTML for the page of the provided link and store it in a Beautiful soup format
# --------------------------------------------------------------------------------------

def allArtistsFirstPage(mainLink):

	firstArtistPage = urllib.urlopen(mainLink)

	formattedFirstArtistPage = BeautifulSoup(firstArtistPage, "html.parser")

	return formattedFirstArtistPage

# ------------------------------------------------------------------
# Find the number of pages on the first page and randomly select one
# ------------------------------------------------------------------

def numberOfPages(formattedFirstPage, mainLink):

	numbers = []
	previous = 0

	pageList = formattedFirstPage.find('ul', {"class" : 'pagelist'})

	if pageList == None:
		print("\nLooks like an incorrect tag was entered! The program will now close.")
		sys.exit()

	# Get a list of page numbers that contains the last page (the largest number of pages that need to be searched)
	for li in pageList:
		item = li.string
		
		if item.isnumeric():
			if item != (1 + previous):
				numberOfPages = int(item)
			else:
				previous = item

	limit = numberOfPages + 1

	# Randomly choose the page number to select the artist from
	randomPageNumber = numpy.random.randint(1, limit)

	url = mainLink + "?page=" + str(randomPageNumber)

	return url

# --------------------------------------------------------------------------------------------
# Create a list of all of the artists on the randomly selected page and randomly select one 
# --------------------------------------------------------------------------------------------

def randomlySelectArtist(url):

	allArtistLinks = []
	artistPage = urllib.urlopen(url)

	formattedArtistPage = BeautifulSoup(artistPage, "html.parser")

	# Find the unordered list where class = "item_list", this contains the relevant code
	allArtistList = formattedArtistPage.find('ul', {"class" : 'item_list'})

	# For the anchor tag in each li element in the ul tag
	for listItem in allArtistList.findAll("a"):
	# Get the link in the href
		artistHomepage = listItem.get("href")
	# Appending /music to the link will insure that all of the artists albums will be presented uniformly to the program
		allArtistLinks.append(artistHomepage)

	length = len(allArtistLinks)
	randomIndex = numpy.random.randint(0, length)

	specificArtistLink = allArtistLinks[randomIndex]

	return specificArtistLink

# ---------------------------------------------------------------------------------------------------
# Find all of the albums an artist has created, randomly select one and present the url to the user
# ---------------------------------------------------------------------------------------------------

def randomlySelectAlbum(specificArtistLink):
	
	artistAlbums = []
	
	searchFor = r'\S*(\.com|\.net|\.uk)'
	artistBaseLink = re.search(searchFor, specificArtistLink)

	unformattedArtistPage = urllib.urlopen(artistBaseLink.group(0))

	formattedArtistPage = BeautifulSoup(unformattedArtistPage, "html.parser")

	albumSection = formattedArtistPage.find('div', {"class" : 'leftMiddleColumns'})

	# Getting the section of code that indicates if the artist has one or multiple albums
	albumNumberCheck = formattedArtistPage.find('div', {"class" : 'trackView'})

	# If the artist has more than one album
	if (albumNumberCheck == None):

		for listItem in albumSection.findAll("a"):
			albumSubLink = listItem.get("href")
			artistAlbums.append(artistBaseLink.group(0) + albumSubLink)

		randomIndex = numpy.random.randint(0, len(artistAlbums))

		selectedAlbum = artistAlbums[randomIndex]

		return selectedAlbum

	# Else the artist has only one album
	else:
		return specificArtistLink

# ------------------------------------------------------------------------
# Get user input if they want a random album or one from a specific tag 
# ------------------------------------------------------------------------

def main():
    if len(sys.argv) >= 2:
        try:
            amount = int(sys.argv[1])
        except ValueError:
            print("That was an invalid input! Program will now close.")
            sys.exit()
    else:
        amount = input("How many albums do you want to download?: ")

        try:
            amount = int(amount)
        except ValueError:
            print("That was an invalid input! Program will now close.")
            sys.exit()

    for x in range(amount):
        mainLink = "https://bandcamp.com/artist_index"

        formattedFirstPage = allArtistsFirstPage(mainLink)
        url = numberOfPages(formattedFirstPage, mainLink)
        artistLink = randomlySelectArtist(url)
        albumLink = randomlySelectAlbum(artistLink)

        print(str(x+1) + ": " + albumLink)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #webbrowser.open(albumLink)
        os.system("bandcamp-dl --base-dir=\"{}\\music\"".format(dir_path) + " --full-album --embed-art --template=\"%{album}/%{track} - %{title}\"" + " {}".format(albumLink))
		

if __name__ == "__main__":
    main()