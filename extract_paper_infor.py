import json
import os
import requests
# import sys
import time
from bs4 import BeautifulSoup

# URL
# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://www.semanticscholar.org/paper/a9c31400520977e0edd854c92edc4efd4f44798f"
# url_paper = "https://api.semanticscholar.org/v1/paper/a9c31400520977e0edd854c92edc4efd4f44798f" # test
code_language = ""
url_code = ""
data_database = ""
url_data = ""


# Send a request to obtain page content
response = requests.get(url_paper)

if url_paper.startswith("https://api.semanticscholar.org"):
    # Extract paper information
    if response.ok:
        try:
            soup = response.json()
            title = soup["title"]
            journal = soup["venue"]
            journal = soup.get("venue", {"raw"})
            journal_doi = soup["doi"]
            journal_doi = f"https://doi.org/{journal_doi}"
            date = soup["year"]
            # abstract = data["abstract"]
            semanticscholar = soup["url"]
        except ValueError as e:
            print(f"Error parsing JSON data: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", {"data-test-id": "paper-detail-title"}).text
    journal = soup.find("span", {"data-heap-id": "paper-meta-journal"}).text
    journal_doi = soup.find("a",
                            {"class":
                             "icon-button button--full-width button--primary flex-paper-actions__button flex-paper-actions__button--primary"})["href"]
    # abstract = soup.find("span", {"data-test-id": "text-truncator-text"}).text.strip()
    date = soup.find("span", {"data-test-id": "paper-year"}).text
    date = date[-4:]
    # citation_count = soup.find(
    #     "span", {"class": "scorecard-stat__headline__dark"}).text
    semanticscholar = soup.find("a",
                                {"class":
                                 "icon-button button--full-width button--primary flex-paper-actions__button flex-paper-actions__button--primary"})["data-heap-paper-id"]

# Merge variables as 'Title'
title = "[" + title + "]" + "(" + journal_doi + ")"

if not url_code:
    url_code = ""
    code_language = "Unknown"
    shields_color_code = "black"
else:
    if code_language == "R":
        shields_color_code = "75aadb"
    elif code_language == "Python":
        shields_color_code = "3572a5"
    elif code_language == "Shell":
        shields_color_code = "89e051"
    elif code_language == "Jupyter Notebook":
        shields_color_code = "da5b0b"
    else:
        code_language = "Unknown"
        shields_color_code = "black"

if " " in code_language:
    code_language = code_language.replace(" ", "%20")
shields_url_code = "https://img.shields.io/badge/-" + \
    code_language + "-" + shields_color_code

# Merge variables as 'Code'
code = "[" + "!" + "[" + code_language + "]" + \
    "(" + shields_url_code + ")" + "]" + "(" + url_code + ")"

if not url_data:
    url_data = ""
    data_database = "Unknown"
    shields_color_data = "black"
else:
    if data_database == "GEO":
        shields_color_data = "336699"
    elif data_database == "Zenodo":
        shields_color_data = "024dad"
    elif data_database == "PKU":
        shields_color_data = "357ca5"
    elif data_database == "figshare":
        shields_color_data = "c62764"
    else:
        data_database = "Unknown"
        shields_color_data = "black"

if " " in data_database:
    data_database = data_database.replace(" ", "%20")
shields_url_data = "https://img.shields.io/badge/-" + \
    data_database + "-" + shields_color_data

# Merge variables as 'Data'
data = "[" + "!" + "[" + data_database + "]" + \
    "(" + shields_url_data + ")" + "]" + "(" + url_data + ")"

semanticscholar_api = "https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F" + \
    semanticscholar + \
    "%3Ffields%3DcitationCount"
semanticscholar_url = ""

# Merge variables as 'Citation'
citation = "[" + "!" + "[" + "citation" + "]" + \
    "(" + semanticscholar_api + ")" + "]" + "(" + url_paper + ")"

# Merge variables as result
result = " | ".join([str(journal),
                     str(date),
                     str(title),
                     str(code),
                     str(data),
                     str(citation)])
result = "| " + result + " |"
# result = "| scientific data | 27 March 2023 | [An integrated single-cell transcriptomic dataset for non-small cell lung cancer](https://www.nature.com/articles/s41597-023-02074-6) | [![R](https://img.shields.io/badge/-R-75aadb)](https://figshare.com/articles/online_resource/NSCLC_data_reanalysis_codes/22106201?backTo=/collections/An_integrated_single-cell_transcriptomic_dataset_for1_non-small_cell_lung_cancer/6222221?backTo=/collections/An_integrated_single-cell_transcriptomic_dataset_for1_non-small_cell_lung_cancer/6222221?backTo=/collections/An_integrated_single-cell_transcriptomic_dataset_for1_non-small_cell_lung_cancer/6222221) | [![figshare](https://img.shields.io/badge/-figshare-c62764)](https://figshare.com/collections/An_integrated_single-cell_transcriptomic_dataset_for1_non-small_cell_lung_cancer/6222221/3) | [![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F2e68442733604d3ff3f9fe5e62201ffc4f1ea951%3Ffields%3DcitationCount)](https://www.semanticscholar.org/paper/An-integrated-single-cell-transcriptomic-dataset-Prazanowska-Lim/2e68442733604d3ff3f9fe5e62201ffc4f1ea951) |"

# Open and write result into markdown file
with open('test.md', 'r+') as f:
    lines = f.readlines()

    # Get the last line and remove the leading and trailing spaces
    last_line = lines[-1].strip()
    f.seek(0, 2)
    f.write("\n" + result)

with open('test.md', 'r+') as f:
    lines = f.readlines()

    # Check whether each row is empty, and if so, delete it
    new_lines = []
    for line in lines:
        if line.strip() != '':
            new_lines.append(line)

    # If the last line is a title, the new content needs to be wrapped
    if new_lines[-1] == os.linesep:
        new_lines.pop()

    # Write the processed content back to the file
    f.seek(0)
    f.write(''.join(new_lines))
    f.truncate()
