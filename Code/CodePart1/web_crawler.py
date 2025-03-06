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
from urllib.parse import urljoin, urlparse
from lingua import Language, LanguageDetectorBuilder


# url, starting urls, and allowed domain of 3 different domains
seed_urls = [
    {
     "url": "https://www.cpp.edu",
     "start_url": "https://www.cpp.edu/",
     "allowed_domain": "cpp.edu",
     "report_file_name": "report1.csv"
     },
    {
       "url": "https://www.lefigaro.fr",
       "start_url": "https://www.lefigaro.fr/",
       "allowed_domain": "lefigaro.fr",
       "report_file_name": "report2.csv"
    },
    {
        "url": "https://www.cervantesvirtual.com",
        "start_url": "https://www.cervantesvirtual.com/",
        "allowed_domain": "cervantesvirtual.com",
        "report_file_name": "report3.csv"
    }
]

# supported languages for the 3 different domains (eng, spanish, french)
supported_langs = {
    Language.ENGLISH: 'en',
    Language.SPANISH: 'es',
    Language.FRENCH: 'fr'
}

detector = LanguageDetectorBuilder.from_languages(
    *supported_langs.keys()).build()  # use the keys as ids of the language

# checks the language of the text, uses the keys to give the language.
def check_lang(text):
    try:
        detected_lang = detector.detect_language_of(text)
        if detected_lang in supported_langs:
            return supported_langs[detected_lang]  # return the selected language code (en, es, fr)
        else:
            return None
    except Exception:
        return None

# Function to check if the domain of the URL matches the allowed domain
def domain_restriction(url, allowed_domain):
    parsed_url = urlparse(url)
    parsed_url = parsed_url.netloc
    # Remove everything up to and including the first dot
    # This way subdomains in the domain will not be restricted
    if '.' in parsed_url:
        parsed_url = parsed_url.split('.', 1)[-1]  # Get the part after the first dot
    return parsed_url == allowed_domain


headers = {"User-Agent": "Mozilla/5.0"}
# main web crawler function
def run_web_crawler(seed_url_info):  # we will get the info from the seed url list in the main program.
    url = seed_url_info["url"]
    start_url = seed_url_info["start_url"]
    allowed_domain = seed_url_info["allowed_domain"]
    report_file_name = seed_url_info["report_file_name"]

    # Create a repository directory
    directory = "repository"
    os.makedirs(directory, exist_ok=True)


    # Send an HTTP GET request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # exception for http errors
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        exit()

    # check the language of the url
    detected_lang = check_lang(response.text)
    if check_lang(response.text):
        print(f"{detected_lang} is supported for ({url})")
    else:
        print(f"Language is not supported for ({url})")

    # Create a BeautifulSoup object which will search through response text
    soup = BeautifulSoup(response.text, "html.parser")

    # Create a file path into the repository folder
    file_path = os.path.join(directory, "0.html")

    # Create a text file with response content in the repository folder
    with open(f"{file_path}", "w") as file:
        file.write(response.text)

    # Find all of the a_tags in web page which contain links
    a_tags = soup.find_all("a", href=True)

    # # Extract href links from the a_tags list
    links = []
    for a in a_tags:
        href = a["href"]
        absolute_url = urljoin(start_url, href)  # Convert relative to absolute
        # If the link contains the domain restriction, add it to the links list
        if domain_restriction(absolute_url, allowed_domain):
            links.append(absolute_url)
            print(absolute_url)  # Debugging output
    #
    # Create the report file and add the first page url and # of links to it
    with open(report_file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([url, len(links)])

    max_links = min(len(links), 49)  # 50 total pages including seed url
    print(f"found {len(links)} links")

    for i in range(max_links):
        try:
            url = links[i]
            # Send an HTTP GET request
            response = requests.get(url, headers=headers)
            # Create a BeautifulSoup object which will search through response text
            soup = BeautifulSoup(response.text, "html.parser")
            # Create a file path into the repository folder
            file_path = os.path.join(directory, f"{i+1}.html")  # start saving the other webpages at 1 to not override seed url
            # Create a text file with response content in the repository folder
            with open(f"{file_path}", "w", encoding="utf-8") as file:
                file.write(response.text)
            # Find all links in web page
            new_links = soup.find_all("a", href=True)
            # Append to the report file and add the url and links of the current web page
            with open(report_file_name, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([url, len(new_links)])
        except Exception as e:
            print(f"error accessing {url}: {e}")

    print(f"Crawling complete. Crawled {max_links + 1} pages")  # uses +1 to include seed url
    if max_links < 49:  # check if max_links is over 50
        print(f"Crawling complete. Found {max_links + 1} pages")
    else:
        print(f"Crawling complete. Processed 50 pages.")

def main():
    for seed_url_info in seed_urls:  # iterating through the seed url info to get the correct info for run_web_crawler
        run_web_crawler(seed_url_info)
    print("Web Crawling Complete.")

if __name__ == "__main__":
    main()