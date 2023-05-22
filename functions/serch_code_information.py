import re
import requests
from bs4 import BeautifulSoup


def format_code(code_language,
                url_code,
                url):
    """
    Format code information: code_language, url_code and url
    """

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
                    code = code_info(code_language, url_code,
                                     shields_color_code)
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


def code_info(code_language,
              url_code,
              shields_color_code):
    """
    This function takes a code_language, url_code, and shields_color_code as arguments and returns a string
    that represents the code.
    """

    # Replace any spaces in the code language with %20
    if " " in code_language:
        code_language = code_language.replace(" ", "%20")

    # Create the code string using the URL and the code language
    shields_url_code = "https://img.shields.io/badge/-" + \
        code_language + "-" + shields_color_code

    # Create the 'Code' string using the parameters
    code = "[" + "!" + "[" + code_language + "]" + \
        "(" + shields_url_code + ")" + "]" + "(" + url_code + ")"
    return code


def check_color(x):
    """
    This function takes a string as an argument and returns a hex code based on the value of the string.
    """

    # Dictionary to store the hex codes for each string
    color_dict = {
        "R": "198ce7",
        "Python": "3572a5",
        "Shell": "89e051",
        "Jupyter Notebook": "da5b0b",
        "GEO": "336699",
        "Zenodo": "024dad",
        "PKU": "357ca5",
        "figshare": "c62764",
        "Failed": "c02f31",
        "Unknown": "ca1fc7"
    }

    # Check if the argument is in the dictionary
    if x not in color_dict:
        x = "Unknown"

    shields_color = color_dict[x]

    return shields_color
