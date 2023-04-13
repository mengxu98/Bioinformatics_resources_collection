
from extract_paper_information import extract_paper_infor

# URL
# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://www.semanticscholar.org/paper/Tumor-microenvironment-remodeling-after-neoadjuvant-Hu-Zhang/dfb50b723e402caac70b0dcbe21ca58e34401505"
# url_paper = "https://api.semanticscholar.org/v1/paper/66d79bafce806798b72b4333854b8761073221cc" # test
code_language = "R Python"
url_code = "https://github.com/Junjie-Hu/NSCLC-immunotherapy"
data_database = "GEO"
url_data = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207422"

extract_paper_infor(url_paper,
                    code_language,
                    url_code,
                    data_database,
                    url_data,
                    file="README.md") # "test.md"
