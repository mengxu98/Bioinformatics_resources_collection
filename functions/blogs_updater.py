import yaml
import os
from datetime import datetime
import re
from itertools import groupby
from typing import Optional
import logging

class BlogsUpdater:
    """Handler for updating blogs.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "blogs.yaml")
        self.md_path = os.path.join(content_dir, "blogs.md")
        self.logger = logging.getLogger(__name__)

    def update_blogs(self):
        """Main method to update blogs.md file"""
        blogs_data = self._read_blogs_yaml()
        grouped_blogs = self._group_blogs_by_field(blogs_data)
        md_content = self._generate_blogs_md(grouped_blogs)
        self._write_blogs_md(md_content)

    def _read_blogs_yaml(self):
        """Read blog entries from blogs.yaml"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _group_blogs_by_field(self, blogs):
        """Group blogs by their field"""
        sorted_blogs = sorted(blogs, key=lambda x: (x['field'].lower(), x['title']))
        return {k: list(g) for k, g in groupby(sorted_blogs, key=lambda x: x['field'])}

    def _get_description(self, blog: dict) -> str:
        """Get blog description from yaml or return a default one"""
        if 'description' in blog and blog['description']:
            return blog['description']
        
        # Return a simple description based on title
        return f"A blog post about {blog['field'].lower()}."

    def _generate_blogs_md(self, grouped_blogs):
        """Generate content for blogs.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Blogs"
author: "Mengxu"
date: {current_time}
lastmod: {current_time}
---

<!--more-->

Here is a curated list of ***Blogs*** covering various topics in bioinformatics, including single-cell RNA sequencing (scRNA-seq), genomics, and related fields. These resources are regularly updated and maintained.

"""
        content = []
        
        # Generate content for each field
        for field, blogs in grouped_blogs.items():
            # Add field as section header
            content.append(f"## {field}\n")
            content.append("| Title | Description |")
            content.append("| -- | -- |")
            
            # Add blogs in this field
            for blog in blogs:
                description = self._get_description(blog)
                content.append(f"| [{blog['title']}]({blog['url']}) | {description} |")
            
            content.append("\n")  # Add space between sections
        
        return header + '\n'.join(content)

    def _write_blogs_md(self, content):
        """Write content to blogs.md file"""
        with open(self.md_path, 'w', encoding='utf-8') as f:
            f.write(content)