'''
This repository is builded and maintained by Mengxu(mengxu98@qq.com).
If you interested it, please add items as follow rules, and PR:
You can choose one of the following ways:

1) Refer to the 'README' file and manually fill in the following information:
    Add "| Journal | Date | Title | Code | Data | Citation |";
        For Journal and Title, please sort by A-Z;
        For Date, please sort by published date;
        For Code and Data, please reference: https://img.shields.io/;
        For Citation, the data of Citation could obtain from: https://www.semanticscholar.org/.

2) Automatically fill in information using 'extract_paper_infor' function:
    Parameter: 'url_paper', need to provide a link to the paper from https://www.semanticscholar.org/;
    Parameter: 'code_language', the main programming languages used in the paper;
    Parameter: 'url_code', code storage address in the paper;
    Parameter: 'data_database', database for storing data in the paper;
    Parameter: 'url_data', data storage address in the paper.

    Note: please shut down the proxy service when using this script!
    
Note: now this script only supports some open access journals correctly, such as "Nature communications", 
        and some journals will not allow extract information.
        So, you should use semanticscholar APIs as much as possible to obtain information,
        and manually fill in other parameters, such as 'code_language', 'url_code', 'data_database' and 'url_data'.

If you encounter any problems while using the script, please issue on GitHub.
'''

# Import function
from extract_paper_information import extract_paper_infor

######################
# ***--- Here ---*** #
######################

# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://www.semanticscholar.org/paper/Tumor-microenvironment-remodeling-after-neoadjuvant-Hu-Zhang/dfb50b723e402caac70b0dcbe21ca58e34401505"
# url_paper = "https://api.semanticscholar.org/v1/paper/66d79bafce806798b72b4333854b8761073221cc"  # test
code_language = "R Python"
url_code = "https://github.com/Junjie-Hu/NSCLC-immunotherapy"
data_database = "GEO"
url_data = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207422"

extract_paper_infor(url_paper,
                    code_language,
                    url_code,
                    data_database,
                    url_data,
                    file="test.md")  # "README.md"
