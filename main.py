"""
This repository is built and maintained by Mengxu(mengxu98@qq.com).
If you interested it, please add items as follows rules, and PR:
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
"""

import logging
from functions.extract_information import extract_paper_infor

logging.basicConfig(level=logging.INFO)


class PaperInfoExtractor:
    def __init__(
        self,
        url_paper,
        doi_paper,
        code_language,
        url_code,
        data_database,
        url_data,
        output_file,
    ):
        self.url_paper = url_paper
        self.doi_paper = doi_paper
        self.code_language = code_language
        self.url_code = url_code
        self.data_database = data_database
        self.url_data = url_data
        self.output_file = output_file

    def extract(self):
        try:
            extract_paper_infor(
                self.url_paper,
                self.doi_paper,
                self.code_language,
                self.url_code,
                self.data_database,
                self.url_data,
                file=self.output_file,
            )
            logging.info("Paper information extracted successfully.")
        except Exception as e:
            logging.error(f"Failed to extract paper information: {e}")


if __name__ == "__main__":    
    import yaml
    
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    
    url_paper = config['paper']['url']
    doi_paper = config['paper']['doi']
    code_language = config['paper']['code_language']
    url_code = config['paper']['url_code']
    data_database = config['paper']['data_database']
    url_data = config['paper']['url_data']
    output_file = config['paper']['output_file']
    
    # url_paper = "https://api.semanticscholar.org/v1/paper/58e4d63a4572ec930429ee65e82ef7c5bf7c593b"
    # doi_paper = [""]
    # code_language = ["R"]
    # url_code = ["https://github.com/Lan-lab/COMSE"]
    # data_database = ["Null"]
    # url_data = [""]
    # output_file = website/content/posts/test.md"
    
    extractor = PaperInfoExtractor(
        url_paper,
        doi_paper,
        code_language,
        url_code,
        data_database,
        url_data,
        output_file
    )
    extractor.extract()
