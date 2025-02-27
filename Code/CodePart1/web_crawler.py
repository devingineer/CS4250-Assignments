# This is an intro web crawler which will crawl CPP home page and download the home page html text and 50 outlinks text
# This program will also generate a report.csv file with the URL and # of outlinks and a repository of all of the page text files
# Features to Add:
#   1. Crawler needs to crawl through different seed URL's
#       ex.) Currently, the only seed URL is Cal Poly Pomona website https://cpp.edu/
#   2. Crawler needs to add domain restrictions
#       ex.) No domain restrictions in this program
#   3.) Crawler does not contain ability to traverse if the initial seed URL has less than 50 links
#       ex.) What happens if the first page only has 10 links? The Crawler must set a new seed URL when traversing
#       if the number of Outlinks if less than 50.

import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

# Create a repository directory
directory = "repository"
os.makedirs(directory, exist_ok=True)

# Cal Poly URL
url = "https://www.cpp.edu"
start_url = "https://www.cpp.edu/"
headers = {"User-Agent": "Mozilla/5.0"}
report_file_name = "report.csv"


# Send an HTTP GET request
response = requests.get(url, headers=headers)

# Create a BeautifulSoup object which will search through response text
soup = BeautifulSoup(response.text, "html.parser")

# Create a file path into the repository folder
file_path = os.path.join(directory, "0.txt")

# Create a text file with response content in the repository folder
with open(f"{file_path}", "w") as file:
    file.write(response.text)

# Find all of the a_tags in web page which contain links
a_tags = soup.find_all("a", href=True)

# Extract href links from the a_tags list
links = []
for a in a_tags:
    href = a["href"]
    absolute_url = urljoin(start_url, href)  # Convert relative to absolute
    links.append(absolute_url)
    print(absolute_url)  # Debugging output

# Create the report file and add the first page url and # of links to it
with open(report_file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([url, len(links)])

# Loop through the link list and add 49 more web pages to the repository and report
for i in range(1, 50):
    url = links[i]

    # Send an HTTP GET request
    response = requests.get(url, headers=headers)

    # Create a BeautifulSoup object which will search through response text
    soup = BeautifulSoup(response.text, "html.parser")

    # Create a file path into the repository folder
    file_path = os.path.join(directory, f"{i}.txt")

    # Create a text file with response content in the repository folder
    with open(f"{file_path}", "w", encoding="utf-8") as file:
        file.write(response.text)

    # Find all links in web page
    new_links = soup.find_all("a", href=True)

    # Append to the report file and add the url and links of the current web page
    with open(report_file_name, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([url, len(new_links)])
