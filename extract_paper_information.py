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
    
    if not file:
        file = "test.md"
    # Open and write result into markdown file
    with open(file, 'r+') as f:
        lines = f.readlines()

        # Get the last line and remove the leading and trailing spaces
        last_line = lines[-1].strip()
        f.seek(0, 2)
        f.write("\n" + result)

    with open(file, 'r+') as f:
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
