def format_shields(code_language, url_code, shields_color_code):
    """
    This function takes a code_language, url_code, and shields_color_code as arguments and returns a string
    that represents the code.
    """

    # Replace any spaces in the code language with %20
    if " " in code_language:
        code_language = code_language.replace(" ", "%20")

    # Create the code string using the URL and the code language
    shields_url_code = (
        "https://img.shields.io/badge/-" + code_language + "-" + shields_color_code
    )

    # Create the 'Code' string using the parameters
    code = (
        "["
        + "!"
        + "["
        + code_language
        + "]"
        + "("
        + shields_url_code
        + ")"
        + "]"
        + "("
        + url_code
        + ")"
    )

    return code


import unittest


class TestFormatShields(unittest.TestCase):
    def test_format_shields_with_spaces_in_code_language(self):
        code_language = "Python"
        url_code = "example.com"
        shields_color_code = "blue"
        expected_result = (
            "[![Python](https://img.shields.io/badge/-Python-blue)](example.com)"
        )
        self.assertEqual(
            format_shields(code_language, url_code, shields_color_code), expected_result
        )

    def test_format_shields_without_spaces_in_code_language(self):
        code_language = "Java"
        url_code = "example.com"
        shields_color_code = "red"
        expected_result = (
            "[![Java](https://img.shields.io/badge/-Java-red)](example.com)"
        )
        self.assertEqual(
            format_shields(code_language, url_code, shields_color_code), expected_result
        )

    def test_format_shields_with_special_characters_in_code_language(self):
        code_language = "R"
        url_code = "example.com"
        shields_color_code = "green"
        expected_result = "[![R](https://img.shields.io/badge/-R-green)](example.com)"
        self.assertEqual(
            format_shields(code_language, url_code, shields_color_code), expected_result
        )


if __name__ == "__main__":
    unittest.main()
