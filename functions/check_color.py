def check_color(string):
    """
    This function takes a string as an argument,
    and returns a hex code based on the value of the string.

    usage:
        check_color("R")
    output:
        '198ce7'
    """

    # Dictionary to store the hex codes for each string
    color_dict = {
        "R": "198ce7",
        "Python": "3572a5",
        "R Python": "00008B",
        "Shell": "89e051",
        "Jupyter Notebook": "da5b0b",
        "GEO": "336699",
        "Zenodo": "024dad",
        "PKU": "357ca5",
        "figshare": "c62764",
        "Website": "B03060",
        "Failed": "c02f31",
        "Unknown": "ADADAD",
        "Null": "FAFAFA"
    }

    # Check if the argument is in the dictionary
    if string not in color_dict:
        string = "Unknown"

    shields_color = color_dict[string]

    return shields_color