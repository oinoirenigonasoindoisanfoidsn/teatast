import urllib.request as urllib
from bs4 import BeautifulSoup
import numpy
import re
import os

# Function to fetch the HTML for a given link and parse it with BeautifulSoup
def fetch_and_parse_html(link):
    page = urllib.urlopen(link)
    return BeautifulSoup(page, "html.parser")

# Function to randomly select an artist's page from the first page
def select_random_artist_page(main_link):
    formatted_first_page = fetch_and_parse_html(main_link)
    page_list = formatted_first_page.find('ul', {"class": 'pagelist'})
    if not page_list:
        print("\nLooks like an incorrect tag was entered! The program will now close.")
        return None
    number_of_pages = len(page_list.find_all("li"))
    random_page_number = numpy.random.randint(1, number_of_pages + 1)
    return f"{main_link}?page={random_page_number}"

# Function to randomly select an artist from a given page
def select_random_artist(url):
    artist_links = []
    artist_page = fetch_and_parse_html(url)
    all_artist_list = artist_page.find('ul', {"class": 'item_list'})
    for list_item in all_artist_list.find_all("a"):
        artist_homepage = list_item.get("href")
        artist_links.append(artist_homepage)
    random_artist_link = numpy.random.choice(artist_links)
    return random_artist_link

# Function to randomly select an album from a given artist
def select_random_album(artist_link):
    artist_albums = []
    search_for = r'\S*(\.com|\.net|\.uk)'
    artist_base_link = re.search(search_for, artist_link)
    unformatted_artist_page = urllib.urlopen(artist_base_link.group(0))
    formatted_artist_page = BeautifulSoup(unformatted_artist_page, "html.parser")
    album_section = formatted_artist_page.find('div', {"class": 'leftMiddleColumns'})
    album_number_check = formatted_artist_page.find('div', {"class": 'trackView'})
    
    if album_number_check is None:
        for list_item in album_section.find_all("a"):
            album_sub_link = list_item.get("href")
            artist_albums.append(artist_base_link.group(0) + album_sub_link)
        random_album_link = numpy.random.choice(artist_albums)
        return random_album_link
    else:
        return artist_link

# Main function to download random albums
def main():
    amount = 4  # Hardcoded to 4 albums
    main_link = "https://bandcamp.com/artist_index"

    for x in range(amount):
        random_artist_page = select_random_artist_page(main_link)
        random_artist_link = select_random_artist(random_artist_page)
        random_album_link = select_random_album(random_artist_link)

        print(f"{x + 1}: {random_album_link}")
        os.system(f"bandcamp-dl --base-dir='./music' --full-album --embed-art --template='%{{album}}/%{{track}} - %{{title}}' {random_album_link}")

if __name__ == "__main__":
    main()
