
from extract_paper_information import extract_paper_infor

# URL
# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://www.semanticscholar.org/paper/a9c31400520977e0edd854c92edc4efd4f44798f"
# url_paper = "https://api.semanticscholar.org/v1/paper/a9c31400520977e0edd854c92edc4efd4f44798f" # test
code_language = ""
url_code = ""
data_database = ""
url_data = ""

extract_paper_infor(url_paper, code_language,
                    url_code, data_database, url_data, file="test.md")
