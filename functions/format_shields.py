def format_shields(code_language,
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
