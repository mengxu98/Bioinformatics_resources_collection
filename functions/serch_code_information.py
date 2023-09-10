import re
import requests
from bs4 import BeautifulSoup

from .check_color import check_color
from .format_shields import format_shields


def format_code(code_language,
                url_code,
                url):
    """
    Format code based on the given parameters.
     Args:
        code_language (str): The language of the code.
        url_code (str): The URL of the code.
        url (str): The URL of the website.
     Returns:
        codes (str): The formatted code information.
    """

    print("Formatting code information......")
    if not url_code and not code_language:
        print("No code information provided......")

        code_infors = search_code(url)

        if code_infors:
            if len(code_infors) == 1:
                code_language = code_infors[0][0]
                url_code = code_infors[0][1]
                shields_color_code = check_color(code_language)
                codes = format_shields(
                    code_language, url_code, shields_color_code)

            else:
                codes = ""
                for code_infor in code_infors:
                    code_language = code_infor[0]
                    url_code = code_infor[1]
                    shields_color_code = check_color(code_language)
                    code = format_shields(code_language, url_code,
                                          shields_color_code)
                    codes = codes + code

        else:
            print("Failed to obtain code information for this paper......")
            # If no code is found
            url_code = ""
            code_language = "Unknown"
            shields_color_code = check_color(code_language)
            codes = format_shields(code_language, url_code, shields_color_code)

    elif url_code and not code_language:
        code_language = "Unknown"
        shields_color_code = check_color(code_language)

        if len(url_code) > 1:
            codes = ""
            for url_code_single in url_code:
                print(f"The code from {url_code_single}......")
                code = format_shields(
                    code_language, url_code_single, shields_color_code)
                codes = codes + code

        else:
            url_code=url_code[0]
            print(f"The code from {url_code}......")
            # If URL code is provided but no code language
            codes = format_shields(code_language, url_code, shields_color_code)

    elif not url_code and code_language:
        # If code language is provided but no URL code
        if len(code_language) > 1:
            codes = ""
            for code_language_single in code_language:
                print(f"The code provided by {code_language_single}......")
                shields_color_code = check_color(code_language_single)
                code = format_shields(code_language_single,
                                      url_code, shields_color_code)
                codes = codes + code

        else:
            code_language=code_language[0]
            print(f"The code provided by {url_code}......")
            # If URL code is provided but no code language
            shields_color_code = check_color(code_language)
            codes = format_shields(code_language, url_code, shields_color_code)

    else:
        if len(code_language) > 1 and len(url_code) > 1:
            if len(code_language) != len(url_code):
                if len(code_language) > len(url_code):
                    for i in range(len(url_code), len(code_language)):
                        url_code.append("")
                if len(code_language) < len(url_code):
                    for i in range(len(code_language), len(url_code)):
                        code_language.append("Unknown")

            codes = ""
            for url_code_single, code_language_single in zip(url_code, code_language):
                print(
                    f"The code provided by {code_language_single}, and from {url_code_single}......")
                shields_color_code = check_color(code_language_single)
                code = format_shields(code_language_single,
                                      url_code_single, shields_color_code)
                codes = codes + code

        else:
            if len(code_language) == 1 and len(url_code) == 1:
                code_language=code_language[0]
                url_code=url_code[0]
                print(
                    f"The code provided by {code_language}, and from {url_code}......")
                # If both code language and URL code are provided
                shields_color_code = check_color(code_language)
                codes = format_shields(
                    code_language, url_code, shields_color_code)

    return codes


def search_code(url):
    """
    Search for code information: code_language, url_code and url
    """

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
            code_link = code_links[0].strip('().')
            if "github.io" in code_link:
                print(
                    f"This code_link: {code_link} maybe not a code repository......")
            else:
                code_infor = check_code_link_class(code_link)
                code_infors.append(code_infor)

    return code_infors


def check_code_link_class(code_link):
    """
    Check if the code link contains "github", "figshare" or "zenodo"
    Note: the code_link should be in the format of "https://github.com/user
    Note: now figshare and zenodo not supported yet, only return 'Unknown' information
    """

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
        code_infor = ["Unknown", code_link]
        return code_infor


def github_filter(code_link):
    """
    Check if the code_link contains "github", "figshare" or "zenodo"
    Note: the code_link should be in the format of "https://github.com/user
    Note: now figshare and zenodo not supported yet, only return 'Unknown' information
    """

    # Check if the code_link starts with "http"
    if code_link.startswith("http"):
        # Replace ".git" with "" if it is found in the code_link
        if ".git" in code_link:
            code_link = code_link.replace(".git", "")

        # Split the code_link to get the owner and repo
        owner, repo = code_link.split("/")[-2:]

        # Create a new code_link for the API request
        new_code_link = f"https://api.github.com/repos/{owner}/{repo}/languages"

        try:
            # Make a request to the API
            languages = requests.get(new_code_link)

            # Check if the response status code is 200 (indicating success)
            if languages.status_code == 200:
                # Obtain response JSON data
                data = languages.json()

                # Traverse the programming language type and its corresponding number of lines, and print it out
                for language, lines in data.items():
                    print(
                        f"Deatiled information: {language}, total {lines} lines")
                    # Return the language and code_link
                    code_infors = [language, code_link]
                    return code_infors
            else:
                print(
                    f"Request failed with status code {languages.status_code}")
                # Return the language and code_link
                code_infors = ["Unknown", code_link]
                return code_infors

        except requests.exceptions.RequestException as e:
            # Handle request errors
            print(f"Request failed with error: {e}")
            code_infors = ["Error", code_link]
            return code_infors

        except ValueError as e:
            # Handle JSON decoding errors
            print(f"JSON decoding failed with error: {e}")
            code_infors = ["Failed", code_link]
            return code_infors

        except:
            # Handle other unknown errors
            print("An unknown error occurred")
            code_infors = ["Failed", code_link]
            return code_infors

    else:
        print(f"This code_link: {code_link} maybe not a code repository......")
        code_infors = ["Unknown", code_link]
        return code_infors
