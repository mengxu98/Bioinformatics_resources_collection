import re
import requests
from bs4 import BeautifulSoup


def search_code(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = response.text

    code_availability = soup.find(
        "div", {"id": "code-availability-content"}).text
    # Regular expression matching link
    pattern = re.compile(
        r'\((http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\)')
    links = re.findall(pattern, code_availability)

    # Traverse all links to check for keywords
    if len(links) > 1:
        for link in links:
            link = link.strip('()')
            if "github.io" in link:
                print(f"This link: {link} maybe not a code repository......")
            else:
                language = check_link_class(link)
    else:
        for link in links:
            link = link.strip('()')
            if "github.io" in link:
                print(f"This link: {link} maybe not a code repository......")
            else:
                language = check_link_class(link)
            code_infor = [language, link]

    return code_infor


def check_link_class(link):
    if "github" in link:
        print("Found a Github repository, link:", link)
        code_infor = github_filter(link)
    elif "figshare" in link:
        print("Found a figshare repository, link:", link)
        github_filter(link)
    elif "zenodo" in link:
        print("Found a zenodo repository, link:", link)
        github_filter(link)
    else:
        print("No repository information......")
    return code_infor


def github_filter(link):
    # Extract the owner username and name of the warehouse
    if ".git" in link:
        link = link.replace(".git", "")
    owner, repo = link.split("/")[-2:]
    newLink = f"https://api.github.com/repos/{owner}/{repo}/languages"
    # Issue a GET request to obtain the programming language type of the warehouse
    languages = requests.get(newLink)
    # Check if the response status code is 200 (indicating success)
    if languages.status_code == 200:
        # Obtain response JSON data
        data = languages.json()
        # Traverse the programming language type and its corresponding number of lines, and print it out
        for language, lines in data.items():
            print(f"Deatiled information: {language}, total {lines} lines")
            code_infor = [language, link]
            return code_infor
    else:
        print(f"Request failed with status code {languages.status_code}")


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
