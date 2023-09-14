#!/usr/bin/env python3

import urllib.request as urllib
from bs4 import BeautifulSoup
import random
import re
import os

def get_random_artist_album():
    mainLink = "https://bandcamp.com/artist_index"
    firstArtistPage = urllib.urlopen(mainLink)
    formattedFirstArtistPage = BeautifulSoup(firstArtistPage, "html.parser")
    pageList = formattedFirstArtistPage.find('ul', {"class": 'pagelist'})
    
    if pageList is None:
        print("\nLooks like an incorrect tag was entered! The program will now close.")
        return

    page_numbers = [int(li.string) for li in pageList if li.string.isnumeric()]
    max_page_number = max(page_numbers)
    
    random_page_number = random.randint(1, max_page_number)
    url = f"{mainLink}?page={random_page_number}"
    artist_links = get_artist_links(url)
    
    if not artist_links:
        return

    specific_artist_link = random.choice(artist_links)
    selected_album = randomly_select_album(specific_artist_link)
    
    return selected_album

def get_artist_links(url):
    artist_links = []
    artistPage = urllib.urlopen(url)
    formattedArtistPage = BeautifulSoup(artistPage, "html.parser")
    allArtistList = formattedArtistPage.find('ul', {"class": 'item_list'})
    
    if allArtistList is None:
        return artist_links

    for listItem in allArtistList.findAll("a"):
        artistHomepage = listItem.get("href")
        artist_links.append(artistHomepage)

    return artist_links

def randomly_select_album(specific_artist_link):
    artistAlbums = []
    searchFor = r'\S*(\.com|\.net|\.uk)'
    artistBaseLink = re.search(searchFor, specific_artist_link)
    unformattedArtistPage = urllib.urlopen(artistBaseLink.group(0))
    formattedArtistPage = BeautifulSoup(unformattedArtistPage, "html.parser")
    albumSection = formattedArtistPage.find('div', {"class": 'leftMiddleColumns'})
    albumNumberCheck = formattedArtistPage.find('div', {"class": 'trackView'})

    if albumNumberCheck is None:
        for listItem in albumSection.findAll("a"):
            albumSubLink = listItem.get("href")
            artistAlbums.append(artistBaseLink.group(0) + albumSubLink)

        return random.choice(artistAlbums)
    else:
        return specific_artist_link

def main():
    for x in range(4):  # Download 4 albums
        album_link = get_random_artist_album()
        
        if album_link:
            print(f"{x + 1}: {album_link}")
            dir_path = os.path.dirname(os.path.realpath(__file__))
            os.system(f"bandcamp-dl --base-dir=\"{dir_path}/music\" --full-album --embed-art --template=\"%{{album}}/%{{track}} - %{{title}}\" {album_link}")

if __name__ == "__main__":
    main()
