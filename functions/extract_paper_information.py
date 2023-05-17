import os
import sys
import requests
from bs4 import BeautifulSoup
from functions.serch_data_information import format_data
from functions.serch_code_information import format_code


'''
import pandas as pd
search_strings = []
# First data frame
df1 = pd.DataFrame({
    "url_paper": [url_paper],
    "doi_paper": [doi_paper],
    "code_language": [code_language],
    "url_code": [url_code],
    "data_database": [data_database],
    "url_data": [url_data]
})
search_strings.append(df1)
search_strings[0]['url_paper'][0]
'''


def extract_papers_infor(search_strings):
    '''
    This function takes a search string and returns a list of the titles,
    authors, year, and code of the paper.

    :param search_string: a string that contains the search term and the
    search term is case insensitive.

    :return: a list of strings that contains the title, author, year, and
    code of the paper.
    '''

    if len(search_strings) > 1:
        print('More than one search term......')


def extract_paper_infor(url_paper, doi_paper, code_language, url_code, data_database, url_data, file="test.md"):
    """
    This function extracts the paper from the specified URL and returns the corresponding information

    Parameters setting:
        Parameter: 'url_paper', need to provide a link of the paper from https://www.semanticscholar.org/;
        Parameter: 'doi_paper', need to provide a doi of the paper;
        Parameter: 'code_language', the main programming languages used of the paper;
        Parameter: 'url_code', code storage address of the paper;
        Parameter: 'data_database', database for storing data of the paper;
        Parameter: 'url_data', data storage address of the paper.

    Returns a list and writes it to the specified *.md file
    """

    if url_paper:
        url_extract = url_paper
    elif not url_paper and doi_paper:
        from semanticscholar import SemanticScholar
        sch = SemanticScholar()
        if "https://doi.org/" in doi_paper:
            doi_paper = doi_paper.replace("https://doi.org/", "")
        paper = sch.get_paper(doi_paper)
        url_extract = paper.url
    else:
        print('Please provide a url of semanticscholar or doi......')
        sys.exit(1)

    # Attempt to make a GET request to the URL
    try:
        response = requests.get(url_extract)
    # If an SSL error occurs, print a message
    except requests.exceptions.SSLError:
        print('Please close the network proxy and try again......')
        sys.exit(1)

    # Extract paper information
    if url_extract.startswith("https://api.semanticscholar.org"):
        # Check if the response status code is 200 (indicating success)
        if response.ok and response.status_code == 200:
            try:
                # Extract the information from soup
                print("Extracting paper information......")
                soup = response.json()
                title = soup["title"]
                journal = soup["venue"]
                journal = soup.get("venue", {"raw"})
                journal_doi = soup["doi"]
                journal_doi = f"https://doi.org/{journal_doi}"
                date = soup["year"]
                # abstract = data["abstract"]
                paper_id = soup["paperId"]
                url_semanticscholar = soup["url"]

                # Print the extracted information
                print("Title:", title)
                print("Published date:", date)
                print("Journal:", journal)
                print("DOI:", journal_doi)

            except ValueError as e:
                print(f"Error parsing JSON data: {e}......")

        else:
            print(
                f"Request failed with status code {response.status_code}......")

    else:
        if response.ok and response.status_code == 200:
            try:
                print("Extracting paper information......")
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.find(
                    "h1", {"data-test-id": "paper-detail-title"}).text
                journal = soup.find(
                    "span", {"data-heap-id": "paper-meta-journal"}).text
                journal_doi = soup.find("a",
                                        {"class":
                                            "icon-button button--full-width button--primary flex-paper-actions__button flex-paper-actions__button--primary"})["href"]
                # abstract = soup.find("span", {"data-test-id": "text-truncator-text"}).text.strip()
                date = soup.find(
                    "span", {"data-test-id": "paper-year"}).text
                date = date[-4:]
                # citation_count = soup.find(
                #     "span", {"class": "scorecard-stat__headline__dark"}).text
                paper_id = soup.find("a",
                                     {"class":
                                      "icon-button button--full-width button--primary flex-paper-actions__button flex-paper-actions__button--primary"})["data-heap-paper-id"]
                url_semanticscholar = f"https://www.semanticscholar.org/paper/{paper_id}"

                # Print the extracted information
                print("Title:", title)
                print("Published date:", date)
                print("Journal:", journal)
                print("DOI:", journal_doi)

            except ValueError as e:
                print(f"Error parsing JSON data: {e}......")
                sys.exit(1)

        else:
            print(
                f"Request failed with status code {response.status_code}......")
            sys.exit(1)
    # Merge variables as 'Title'
    title = "[" + title + "]" + "(" + journal_doi + ")"

    # Merge variables as 'Code'
    code = format_code(code_language, url_code, journal_doi)

    # Merge variables as 'Data'
    data = format_data(data_database, url_data, journal_doi)

    # Merge variables as 'semanticscholar_api'
    semanticscholar_api = "https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F" + \
        paper_id + \
        "%3Ffields%3DcitationCount"

    # Merge variables as 'Citation'
    citation = "[" + "!" + "[" + "citation" + "]" + \
        "(" + semanticscholar_api + ")" + "]" + "(" + url_semanticscholar + ")"

    # Merge variables as 'Result'
    result = " | ".join([str(journal),
                        str(date),
                        str(title),
                        str(code),
                        str(data),
                        str(citation)])
    result = "| " + result + " |"
    print("Extracting paper information done......")

    # Check if the file exists
    print(f"Checking {file} existence......")
    if not file:
        file = "test.md"

    # Check if the file exists
    if not os.path.exists(file):
        # Create the file and write a header
        with open(file, 'w') as f:
            f.write('# Papers with code\n### A repository of Papers-With-Code\n| Journal | Date | Title | Code | Data | Citation |\n| -- | -- | -- | -- | -- | -- |\n')
            print(f'The {file} created successfully......')
    else:
        print(f'The {file} already exists......')

    print(f'Write information to {file}......')
    with open(file, 'r+') as f:
        # Read all lines from the file
        lines = f.readlines()

        # Get the last line of the file
        # last_line = lines[-1].strip()

        # Move the pointer to the end of the file
        f.seek(0, 2)

        # Write the result to the end of the file
        f.write("\n" + result)

    # Open the file again in read/write mode
    with open(file, 'r+') as f:
        # Read all lines from the file
        lines = f.readlines()

        # Create a new list with non-empty lines
        new_lines = []
        for line in lines:
            if line.strip() != '':
                new_lines.append(line)

        # Remove the last line if it is an empty line
        if new_lines[-1] == os.linesep:
            new_lines.pop()

        # Move the pointer to the beginning of the file
        f.seek(0)

        # Write the new lines to the file
        f.write(''.join(new_lines))

        # Truncate the file
        f.truncate()
