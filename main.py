'''
This repository is builded and maintained by Mengxu(mengxu98@qq.com).
If you interested it, please add items as follow rules, and PR:
You can choose one of the following two ways:

1) Automatically fill in information using 'extract_paper_infor' function:
    Parameters setting:
        Parameter: 'url_paper', need to provide a link of the paper from https://www.semanticscholar.org/;
        Parameter: 'doi_paper', need to provide a doi of the paper;
        Parameter: 'code_language', the main programming languages used of the paper;
        Parameter: 'url_code', code storage address of the paper;
        Parameter: 'data_database', database for storing data of the paper;
        Parameter: 'url_data', data storage address of the paper.

    Note: please shut down the proxy service when using this script!!!
         
    Note: now this script only supports some open access journals correctly, such as "Nature communications", 
        and some journals will not allow extract information.
        So, you should use semanticscholar APIs as much as possible to obtain information,
        and manually fill in other parameters, such as 'code_language', 'url_code', 'data_database' and 'url_data'.

2) Refer to the 'README' file and manually fill in the following information:
    Add "| Journal | Date | Title | Code | Data | Citation |";
        For Journal and Title, please sort by A-Z;
        For Date, please sort by published date;
        For Code and Data, please reference: https://img.shields.io/;
        For Citation, the data of Citation could obtain from: https://www.semanticscholar.org/.

If you encounter any problems when using this script, please issue on GitHub or contact me.
'''


# Import function
from functions.extract_information import extract_paper_infor

# The URL of paper obtain from: https://www.semanticscholar.org/
url_paper = "https://api.semanticscholar.org/v1/paper/806cfebf4f12d190197101608d7fe140f8edadb8"
doi_paper = ['']
code_language = ['R']
url_code = ['https://github.com/One-Biosciences/MAYA/']
data_database = ['None']
url_data = ['None']


extract_paper_infor(url_paper,
                    doi_paper,
                    code_language,
                    url_code,
                    data_database,
                    url_data,
                    file="papers/papers-with-method.md") # "papers/papers-with-story.md"
