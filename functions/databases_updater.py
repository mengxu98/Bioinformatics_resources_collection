import yaml
import os
from datetime import datetime
import re
from itertools import groupby
import logging

class DatabasesUpdater:
    """Handler for updating databases.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "databases.yaml")
        self.md_path = os.path.join(content_dir, "databases.md")
        self.logger = logging.getLogger(__name__)

    def update_databases(self):
        """Main method to update databases.md file"""
        databases_data = self._read_databases_yaml()
        grouped_databases = self._group_databases_by_field(databases_data)
        md_content = self._generate_databases_md(grouped_databases)
        self._write_databases_md(md_content)

    def _read_databases_yaml(self):
        """Read database entries from databases.yaml"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _group_databases_by_field(self, databases):
        """Group databases by their field"""
        # Split combined fields and create separate entries
        expanded_databases = []
        for db in databases:
            fields = [f.strip() for f in db['field'].split(',')]
            for field in fields:
                db_copy = db.copy()
                db_copy['field'] = field
                expanded_databases.append(db_copy)
        
        sorted_databases = sorted(expanded_databases, key=lambda x: (x['field'].lower(), x['title']))
        return {k: list(g) for k, g in groupby(sorted_databases, key=lambda x: x['field'])}

    def _generate_databases_md(self, grouped_databases):
        """Generate content for databases.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Databases"
author: "Mengxu"
date: {current_time}
lastmod: {current_time}
---

<!--more-->

Here is a curated list of ***Databases*** covering various topics in bioinformatics, including single-cell RNA sequencing (scRNA-seq), genomics, and related fields. These resources are regularly updated and maintained.

"""
        content = []
        
        # Generate content for each field
        for field, databases in grouped_databases.items():
            # Add field as section header
            content.append(f"## {field}\n")
            content.append("| Database | Description | Related Paper |")
            content.append("| -- | -- | -- |")
            
            # Add databases in this field
            for db in databases:
                paper_link = f"[paper]({db['paper_url']})" if 'paper_url' in db and db['paper_url'] else ""
                content.append(f"| [{db['title']}]({db['url']}) | {db['description']} | {paper_link} |")
            
            content.append("\n")  # Add space between sections
        
        return header + '\n'.join(content)

    def _write_databases_md(self, content):
        """Write content to databases.md file"""
        with open(self.md_path, 'w', encoding='utf-8') as f:
            f.write(content) 