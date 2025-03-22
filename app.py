import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def is_valid_url(base, url):
    """ Check if the URL belongs to the same domain """
    return urlparse(url).netloc == urlparse(base).netloc

def get_all_urls(base_url):
    """ Extract all relevant URLs from a webpage within the same domain """
    urls = set()
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(base_url, href)
        if is_valid_url(base_url, href):
            urls.add(href)
    return list(urls)

def extract_text(url):
    """ Extract and return the text from a webpage """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.get_text()

def main():
    base_url = 'https://www.riverbankcomputing.com/static/Docs/PyQt5/'
    urls = get_all_urls(base_url)
    all_text = ""
    
    for url in urls:
        all_text += extract_text(url)
        all_text += "\n\n"  # Separate texts from different pages
    
    # Save the compiled text into a file
    with open("compiled_documentation.txt", "w", encoding="utf-8") as file:
        file.write(all_text)

if __name__ == "__main__":
    main()
