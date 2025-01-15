import os
import sys
import requests
from bs4 import BeautifulSoup
import re

def get_album_links():
    """Fetch album links from the random album page."""
    url = 'https://random-album.com/'

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Successfully fetched the page: {url}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags with href attribute
        links = soup.find_all('a', href=True)

        # Filter links that match the /album pattern
        album_links = []
        for link in links:
            href = link['href']
            if '/album' in href:
                if href.startswith('/'):
                    full_url = f"https://{href[2:]}" if href[2:] else f"https://{href[1:]}"
                else:
                    full_url = href
                album_links.append(full_url)

        return album_links
    else:
        print(f"Failed to fetch the page: {url}, Status Code: {response.status_code}")
        return []

def download_albums(album_links, num_albums):
    """Download specified number of albums using bandcamp-dl."""
    num_downloaded = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))

    for link in album_links:
        if num_downloaded >= num_albums:
            break
        print(f"Downloading album: {link}")
        os.system(f"{dir_path}/venforscript/bin/bandcamp-dl --base-dir=\"{dir_path}/music\" --full-album --embed-art --template=\"%{{album}}/%{{track}} - %{{title}}\" {link}")
        num_downloaded += 1

    if num_downloaded == 0:
        print("No albums downloaded.")
    else:
        print(f"Downloaded {num_downloaded} album(s).")

def main():
    # Check if a number is passed as a command-line argument
    if len(sys.argv) > 1:
        try:
            num_iterations = int(sys.argv[1])
            print(f"Number of iterations to run: {num_iterations} (from command-line)")
        except ValueError:
            print("Invalid number parameter provided. Please enter a valid integer.")
            return
    else:
        try:
            num_iterations = int(input("Enter the number of iterations to run: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return

    for i in range(num_iterations):
        print(f"Iteration {i + 1} of {num_iterations}")
        album_links = get_album_links()

        if album_links:
            print(f"Found {len(album_links)} album(s). Downloading...")
            download_albums(album_links, len(album_links))
        else:
            print("No album links found.")

if __name__ == '__main__':
    main()
