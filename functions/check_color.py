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
        "MATLAB": "e16737",
        "R Python": "00008B",
        "Shell": "89e051",
        "Jupyter Notebook": "da5b0b",
        "GEO": "336699",
        "Zenodo": "024dad",
        "PKU": "357ca5",
        "figshare": "c62764",
        "UK Biobank": "005f6f",
        "ADNI": "34791f",
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


import unittest

class TestCheckColor(unittest.TestCase):
    def test_check_color(self):
        self.assertEqual(check_color("R"), "198ce7")
        self.assertEqual(check_color("Python"), "3572a5")
        self.assertEqual(check_color("MATLAB"), "e16737")
        self.assertEqual(check_color("R Python"), "00008B")
        self.assertEqual(check_color("Shell"), "89e051")
        self.assertEqual(check_color("Jupyter Notebook"), "da5b0b")
        self.assertEqual(check_color("GEO"), "336699")
        self.assertEqual(check_color("Zenodo"), "024dad")
        self.assertEqual(check_color("PKU"), "357ca5")
        self.assertEqual(check_color("figshare"), "c62764")
        self.assertEqual(check_color("UK Biobank"), "005f6f")
        self.assertEqual(check_color("ADNI"), "34791f")
        self.assertEqual(check_color("Website"), "B03060")
        self.assertEqual(check_color("Failed"), "c02f31")
        self.assertEqual(check_color("Unknown"), "ADADAD")
        self.assertEqual(check_color("Null"), "FAFAFA")

if __name__ == '__main__':
    unittest.main()
