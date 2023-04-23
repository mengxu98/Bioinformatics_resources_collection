import re
import requests
from bs4 import BeautifulSoup


def format_data(data_language, url_data, url):
    """
    Format data based on the given parameters.
     Args:
        data_language (str): The language of the data.
        url_data (str): The URL of the data.
        url (str): The URL of the website.
     Returns:
        datas (str): The formatted data.
    """

    print("Formatting data......")
    if not url_data and not data_language:
        print("No data information provided......")
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
                    data = data_info(data_language, url_data,
                                     shields_color_data)
                    datas = datas + data

        else:
            # If no data is found
            url_data = ""
            data_language = "Unknown"
            shields_color_data = check_color(data_language)
            datas = data_info(data_language, url_data, shields_color_data)

    elif url_data and not data_language:
        # If URL data is provided but no data language
        data_language = "Unknown"
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)

    elif not url_data and data_language:
        # If data language is provided but no URL data
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)

    else:
        # If both data language and URL data are provided
        shields_color_data = check_color(data_language)
        datas = data_info(data_language, url_data, shields_color_data)
    return datas


def search_databases(url):
    print("Searching for databases......")
    response = requests.get(url)
    content = response.text
    data_infors = []

    # search for GEO database identifiers using regular expressions
    print("Searching for GEO database identifiers......")
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


def data_info(data_language, url_data, shields_color_data):
    """
    This function takes three parameters: data_language, url_data and shields_color_data
    """

    # Replace any spaces in the data language with %20
    if " " in data_language:
        data_language = data_language.replace(" ", "%20")

    # Create the shields_url_data using the parameters
    shields_url_data = "https://img.shields.io/badge/-" + \
        data_language + "-" + shields_color_data

    # Create the 'Data' string using the parameters
    data = "[" + "!" + "[" + data_language + "]" + \
        "(" + shields_url_data + ")" + "]" + "(" + url_data + ")"
    return data


def check_color(x):
    """
    This function takes a string as an argument and returns a hex code based on the value of the string.
    """

    # Dictionary to store the hex codes for each string
    color_dict = {
        "R": "75aadb",
        "Python": "3572a5",
        "Shell": "89e051",
        "Jupyter Notebook": "da5b0b",
        "GEO": "336699",
        "Zenodo": "024dad",
        "PKU": "357ca5",
        "figshare": "c62764",
        "Failed": "c02f31"
    }
    # Check if the argument is in the dictionary
    if x in color_dict:
        shields_color = color_dict[x]
    else:
        x = "Unknown"
        shields_color = "ca1fc7"
    return shields_color
