import yaml
import os
from datetime import datetime
import re
from itertools import groupby
import logging

class LabsUpdater:
    """Handler for updating labs.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "labs.yaml")
        self.md_path = os.path.join(content_dir, "labs.md")
        self.logger = logging.getLogger(__name__)

    def update_labs(self):
        """Main method to update labs.md file"""
        labs_data = self._read_labs_yaml()
        grouped_labs = self._group_labs_by_field(labs_data)
        md_content = self._generate_labs_md(grouped_labs)
        self._write_labs_md(md_content)

    def _read_labs_yaml(self):
        """Read lab entries from labs.yaml"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _group_labs_by_field(self, labs):
        """Group labs by their field"""
        sorted_labs = sorted(labs, key=lambda x: (x['field'].lower(), x['title']))
        return {k: list(g) for k, g in groupby(sorted_labs, key=lambda x: x['field'])}

    def _generate_labs_md(self, grouped_labs):
        """Generate content for labs.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Labs"
author: "Mengxu"
date: {current_time}
lastmod: {current_time}
---

<!--more-->

Here is a curated list of ***Labs*** conducting research in bioinformatics, single-cell RNA sequencing (scRNA-seq), and related fields. Each lab is listed with their notable contributions and tools.

"""
        content = []
        
        # Generate content for each field
        for field, labs in grouped_labs.items():
            # Add field as section header
            content.append(f"## {field}\n")
            content.append("| Lab | Masterpiece | Description |")
            content.append("| -- | -- | -- |")
            
            # Add labs in this field
            for lab in labs:
                lab_link = f"[{lab['title']}]({lab['url']})"
                masterpiece = (f"[{lab['masterpiece']}]({lab['masterpiece_url']})" 
                             if 'masterpiece' in lab and 'masterpiece_url' in lab 
                             else "")
                description = lab.get('description', "")
                
                content.append(f"| {lab_link} | {masterpiece} | {description} |")
            
            content.append("\n")  # Add space between sections
        
        return header + '\n'.join(content)

    def _write_labs_md(self, content):
        """Write content to labs.md file"""
        with open(self.md_path, 'w', encoding='utf-8') as f:
            f.write(content) 