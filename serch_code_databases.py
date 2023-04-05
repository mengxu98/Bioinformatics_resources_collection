import re
import requests
from bs4 import BeautifulSoup


def search_code(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # content = response.text

    code_availability = soup.find(
        "div", {"id": "code-availability-content"}).text
    # Regular expression matching code_link
    pattern = re.compile(
        r'\((http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\)')
    code_links = re.findall(pattern, code_availability)
    code_links = list(set(code_links))
    # Traverse all code_links to check for keywords
    if len(code_links) > 1:
        code_infors = []
        for code_link in code_links:
            code_link = code_link.strip('()')
            if "github.io" in code_link:
                print(
                    f"This code_link: {code_link} maybe not a code repository......")
            else:
                language = check_code_link_class(code_link)
                code_infor = [language, code_link]
                code_infors.append(code_infor)
    else:
        code_link = code_links.strip('()')
        if "github.io" in code_link:
            print(
                f"This code_link: {code_link} maybe not a code repository......")
        else:
            language = check_code_link_class(code_link)
            code_infors = [language, code_link]

    return code_infors


def check_code_link_class(code_link):
    if "github" in code_link:
        print("Found a Github repository, code_link:", code_link)
        code_infors = github_filter(code_link)
    elif "figshare" in code_link:
        print("Found a figshare repository, code_link:", code_link)
    elif "zenodo" in code_link:
        print("Found a zenodo repository, code_link:", code_link)
    else:
        print("No repository information......")
    return code_infors


def github_filter(code_link):
    # Extract the owner username and name of the warehouse
    if ".git" in code_link:
        code_link = code_link.replace(".git", "")
    owner, repo = code_link.split("/")[-2:]
    new_code_link = f"https://api.github.com/repos/{owner}/{repo}/languages"
    # Issue a GET request to obtain the programming language type of the warehouse
    languages = requests.get(new_code_link)
    # Check if the response status code is 200 (indicating success)
    if languages.status_code == 200:
        # Obtain response JSON data
        data = languages.json()
        # Traverse the programming language type and its corresponding number of lines, and print it out
        for language, lines in data.items():
            print(f"Deatiled information: {language}, total {lines} lines")
            code_infors = [language, code_link]
            return code_infors
    else:
        print(f"Request failed with status code {languages.status_code}")


def search_databases(url):
    response = requests.get(url)
    content = response.text
    data_infors = []
    # search for GEO database identifiers using regular expressions
    geo_ids = re.findall(r"(?i)GSE[\d]+", content)
    if geo_ids:
        unique_geo_ids = list(set(geo_ids))  # Remove Duplicates
        if len(unique_geo_ids) > 1:
            for geo_id in unique_geo_ids:
                geo_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=" + geo_id
                print(f"Found GEO database identifier(s):{geo_url}")
                data_infor = ["GEO", geo_url]
                data_infors.append(data_infor)
        else:
            geo_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=" + geo_id
            print(f"Found GEO database identifier(s):{geo_url}")
            data_infor = ["GEO", geo_url]
            data_infors.append(data_infor)

    # search for Zenodo database identifiers using regular expressions
    zenodo_ids = re.findall(r"(?i)zenodo.org/record/\d+", content)
    if zenodo_ids:
        unique_zenodo_ids = list(set(zenodo_ids))  # Remove Duplicates
        if len(unique_zenodo_ids) > 1:
            for zenodo_id in unique_geo_ids:
                zenodo_url = "https://doi.org/" + zenodo_id
                data_infor = ["Zenodo", zenodo_url]
                data_infors.append(data_infor)
        else:
            zenodo_url = "https://doi.org/" + zenodo_id
            data_infor = ["Zenodo", zenodo_url]
            data_infors.append(data_infor)

    # if the website contains Zenodo link, search for the DOI
    elif re.search(r"zenodo", content):
        zenodo_ids = re.findall(r'10\.\d+\/zenodo\.\d+', content)
        if zenodo_ids:
            unique_zenodo_ids = list(set(zenodo_ids))  # Remove Duplicates
            if len(unique_zenodo_ids) > 1:
                for zenodo_id in unique_zenodo_ids:
                    zenodo_url = "https://doi.org/" + zenodo_id
                    data_infor = ["Zenodo", zenodo_url]
                    data_infors.append(data_infor)
            else:
                zenodo_url = "https://doi.org/" + zenodo_id
                data_infor = ["Zenodo", zenodo_url]
                data_infors.append(data_infor)
    else:
        print("The website does not contain Zenodo link.")

    # search for Figshare database identifiers using regular expressions
    figshare_ids = re.findall(r"(?i)figshare.com/articles/\w+/\d+", content)
    if figshare_ids:
        unique_figshare_ids = list(set(figshare_ids))  # Remove Duplicates
        if len(unique_figshare_ids) > 1:
            for figshare_id in unique_figshare_ids:
                figshare_url = "https://doi.org/" + figshare_id
                data_infor = ["figshare", figshare_url]
                data_infors.append(data_infor)
        else:
            figshare_url = "https://doi.org/" + figshare_id
            data_infor = ["figshare", figshare_url]
            data_infors.append(data_infor)

    return data_infors
