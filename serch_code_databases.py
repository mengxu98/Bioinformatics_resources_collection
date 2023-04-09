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
    pattern = r"(?P<url>https?://\S+)[\s.]"
    code_links = re.findall(pattern, code_availability)
    code_links = list(set(code_links))

    code_infors = []
    if code_links:
        # Traverse all code_links to check for keywords
        if len(code_links) > 1:
            for code_link in code_links:
                code_link = code_link.strip('(.)')
                if "github.io" in code_link:
                    print(
                        f"This code_link: {code_link} maybe not a code repository......")
                else:
                    code_infor = check_code_link_class(code_link)
                    code_infors.append(code_infor)
        else:
            code_link = code_links.strip('()')
            if "github.io" in code_link:
                print(
                    f"This code_link: {code_link} maybe not a code repository......")
            else:
                code_infor = check_code_link_class(code_link)
                code_infors.append(code_infor)
    return code_infors


def check_code_link_class(code_link):
    if "github" in code_link:
        print("Found a Github repository, code_link:", code_link)
        code_infor = github_filter(code_link)
        return code_infor
    elif "figshare" in code_link:
        print("Found a figshare repository, code_link:", code_link)
        code_infor = ["figshare", code_link]
        return code_infor
    elif "zenodo" in code_link:
        print("Found a zenodo repository, code_link:", code_link)
        code_infor = ["zenodo", code_link]
        return code_infor
    else:
        print("No repository information......")


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
        code_infors = ["Unkonw", code_link]
        return code_infors


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


def code_info(code_language, url_code, shields_color_code):
    if " " in code_language:
        code_language = code_language.replace(" ", "%20")
    shields_url_code = "https://img.shields.io/badge/-" + \
        code_language + "-" + shields_color_code

    # Merge variables as 'Code'
    code = "[" + "!" + "[" + code_language + "]" + \
        "(" + shields_url_code + ")" + "]" + "(" + url_code + ")"
    return code

def format_code(code_language, url_code, url):
    if not url_code and not code_language:
        code_infors = search_code(url)
        if code_infors:
            if len(code_infors) == 1:
                code_language = code_infors[0][0]
                url_code = code_infors[0][1]
                shields_color_code = check_color(code_language)
                codes = code_info(code_language, url_code, shields_color_code)
                
            else:
                codes = ""
                for code_infor in code_infors:
                    code_language = code_infor[0]
                    url_code = code_infor[1]
                    shields_color_code = check_color(code_language)
                    code = code_info(code_language, url_code, shields_color_code)
                    codes = codes + code
                
        else:
            url_code = ""
            code_language = "Unknown"
            shields_color_code = check_color(code_language)
            codes = code_info(code_language, url_code, shields_color_code)
    elif url_code and not code_language:
        code_language = "Unknown"
        shields_color_code = check_color(code_language)
        codes = code_info(code_language, url_code, shields_color_code)
    elif not url_code and code_language:
        shields_color_code = check_color(code_language)
        codes = code_info(code_language, url_code, shields_color_code)
    else:
        shields_color_code = check_color(code_language)
        codes = code_info(code_language, url_code, shields_color_code)
    return codes


def data_info(data_language, url_data, shields_color_data):
    if " " in data_language:
        data_language = data_language.replace(" ", "%20")
    shields_url_data = "https://img.shields.io/badge/-" + \
        data_language + "-" + shields_color_data

    # Merge variables as 'data'
    data = "[" + "!" + "[" + data_language + "]" + \
        "(" + shields_url_data + ")" + "]" + "(" + url_data + ")"
    return data

def format_data(data_language, url_data, url):
    if not url_data and not data_language:
        data_infors = search_databases(url)
        if data_infors:
            if len(data_infors) == 1:
                data_language = data_infors[0][0]
                url_data = data_infors[0][1]
                shields_color_data = check_color(data_language)
                datas = data_info(data_language, url_data, shields_color_data)
                
            else:
                datas = ""
                for data_infor in data_infors:
                    data_language = data_infor[0]
                    url_data = data_infor[1]
                    shields_color_data = check_color(data_language)
                    data = data_info(data_language, url_data, shields_color_data)
                    datas = datas + data
                
        else:
            url_data = ""
            data_language = "Unknown"
            shields_color_data = check_color(data_language)
            datas = data_info(data_language, url_data, shields_color_data)
    elif url_data and not data_language:
        data_language = "Unknown"
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)
    elif not url_data and data_language:
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)
    else:
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)
    return datas


def check_color(x):
    if x == "R":
        shields_color = "75aadb"
    elif x == "Python":
        shields_color = "3572a5"
    elif x == "Shell":
        shields_color = "89e051"
    elif x == "Jupyter Notebook":
        shields_color = "da5b0b"
    elif x == "GEO":
        shields_color = "336699"
    elif x == "Zenodo":
        shields_color = "024dad"
    elif x == "PKU":
        shields_color = "357ca5"
    elif x == "figshare":
        shields_color = "c62764"
    else:
        x = "Unknown"
        shields_color = "black"
    return shields_color