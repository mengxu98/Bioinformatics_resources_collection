+++
author = "Mengxu"
title = "Description"
date = "2019-03-09"
description = "Lorem Ipsum Dolor Si Amet"
tags = [
    "markdown",
    "text",
]
+++

# *Papers with code*
This repository is used to record same papers with different categories, such as, bioinformatics methods (main) in [`Papers with method`](/papers/papers-with-method.md) and biology stories in [`Papers with story`](/papers/papers-with-story.md) of single-cell omics data.
<!--more-->

## Maintenance
This repository is builded and maintained by Mengxu(mengxu98@qq.com).
If you interested it, please add items as follow rules, and PR:
You can choose one of the following ways:
1) Refer the 'README' file and manually fill in the following information:
    - Add "| Journal | Date | Title | Code | Data | Citation |";
    - For Journal and Title, please sort by A-Z;
    - For Date, please sort by published date;
    - For Code and Data, please reference: https://img.shields.io/;
    - For Citation, the data of Citation could obtain from: https://www.semanticscholar.org/.

2) Automatically fill in information using 'extract_paper_infor' function:
    - Parameter: 'url_paper', need to provide a link to the paper from https://www.semanticscholar.org/;
    - Parameter: 'code_language', the main programming languages used in the paper;
    - Parameter: 'url_code', code storage address in the paper;
    - Parameter: 'data_database', database for storing data in the paper;
    - Parameter: 'url_data', data storage address in the paper.

    Note:
    - Using ```pip install -r requirements.txt``` to get all the dependencies
    - Please shut down the `proxy` service when using this script!
    - If you encounter any problems while using the script, please issue on GitHub.

