
from extract_paper_information import extract_paper_infor

# URL
# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://www.semanticscholar.org/paper/Single-cell-RNA-sequencing-reveals-distinct-tumor-Bischoff-Trinks/66d79bafce806798b72b4333854b8761073221cc"
# url_paper = "https://api.semanticscholar.org/v1/paper/66d79bafce806798b72b4333854b8761073221cc" # test
code_language = ""
url_code = ""
data_database = ""
url_data = ""

extract_paper_infor(url_paper,
                    code_language,
                    url_code,
                    data_database,
                    url_data,
                    file="test.md") # "README.md"
