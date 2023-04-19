import os
import requests
from bs4 import BeautifulSoup
from serch_code_databases import format_data
from serch_code_databases import format_code


def extract_paper_infor(url_paper, code_language, url_code, data_database, url_data, file="test.md"):

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
        journal = soup.find(
            "span", {"data-heap-id": "paper-meta-journal"}).text
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

    code = format_code(code_language, url_code, journal_doi)
    data = format_data(data_database, url_data, journal_doi)

    # Merge variables as 'Citation'
    semanticscholar_api = "https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F" + \
        semanticscholar + \
        "%3Ffields%3DcitationCount"

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

    # open the file in read/write mode
    if not file:
        file = "test.md"
        
    if os.path.exists(file):
        open(file, 'w').close()

    with open(file, 'r+') as f:
        # read all lines from the file
        lines = f.readlines()
        # get the last line of the file
        last_line = lines[-1].strip()
        # move the pointer to the end of the file
        f.seek(0, 2)
        # write the result to the end of the file
        f.write("\n" + result)
    # open the file again in read/write mode
    with open(file, 'r+') as f:
        # read all lines from the file
        lines = f.readlines()
        # create a new list with non-empty lines
        new_lines = []
        for line in lines:
            if line.strip() != '':
                new_lines.append(line)
        # remove the last line if it is an empty line
        if new_lines[-1] == os.linesep:
            new_lines.pop()
        # move the pointer to the beginning of the file
        f.seek(0)
        # write the new lines to the file
        f.write(''.join(new_lines))
        # truncate the file
        f.truncate()
