import re
import requests
from bs4 import BeautifulSoup


def search_code(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # content = response.text
    codeAvailability = soup.find(
        "div", {"id": "code-availability-content"}).text
    # Regular expression matching link
    pattern = re.compile(
        r'\((http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\)')
    links = re.findall(pattern, codeAvailability)

    
    if len(links) > 1:
        for link in links:
            link = link.strip('()')
    else:
        for link in links:
            link = link.strip('()')
    languages = requests.get(link)
    languages = BeautifulSoup(languages, "html.parser")

    code_links = ["github", "figshare", "zenodo"]
    for code in code_links:

        # Convert the text and the word you want to find to lowercase, and use the split () method to split the text into a word list
        link = code.lower().split()
        code = code.lower()

        # Traverse all links to check for keywords
        for link in links:
            if code in link:
                print("Found a", code, "link:", link)


def search_databases(url):
    response = requests.get(url)
    content = response.text

    # search for GEO database identifiers using regular expressions
    geo_ids = re.findall(r"(?i)GEO[\d]+", content)
    if geo_ids:
        print("Found GEO database identifier(s):")
        for id in geo_ids:
            print(id)

    # search for Zenodo database identifiers using regular expressions
    zenodo_ids = re.findall(r"(?i)zenodo.org/record/\d+", content)
    if zenodo_ids:
        print("Found Zenodo database identifier(s):")
        for id in zenodo_ids:
            print(id)
    # if the website contains Zenodo link, search for the DOI
    elif re.search(r"zenodo", content):
        match = re.findall(r'10\.\d+\/zenodo\.\d+', content)
        if len(match) > 0:
            first_doi = match[0]
            print(
                "The paper can be directly searched on Zenodo: https://doi.org/" + first_doi)
        else:
            print("No Zenodo DOI found in the text.")
    else:
        print("The website does not contain Zenodo link.")

    # search for Figshare database identifiers using regular expressions
    figshare_ids = re.findall(r"(?i)figshare.com/articles/\w+/\d+", content)
    if figshare_ids:
        print("Found Figshare database identifier(s):")
        for id in figshare_ids:
            print(id)
