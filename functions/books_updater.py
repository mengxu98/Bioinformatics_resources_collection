import yaml
import os
from datetime import datetime
import re
from itertools import groupby
import logging

class BooksUpdater:
    """Handler for updating books.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "books.yaml")
        self.md_path = os.path.join(content_dir, "books.md")
        self.logger = logging.getLogger(__name__)

    def update_books(self):
        """Main method to update books.md file"""
        books_data = self._read_books_yaml()
        grouped_books = self._group_books_by_field(books_data)
        md_content = self._generate_books_md(grouped_books)
        self._write_books_md(md_content)

    def _read_books_yaml(self):
        """Read book entries from books.yaml"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _group_books_by_field(self, books):
        """Group books by their field"""
        sorted_books = sorted(books, key=lambda x: (x['field'].lower(), x['title']))
        return {k: list(g) for k, g in groupby(sorted_books, key=lambda x: x['field'])}

    def _get_description(self, book: dict) -> str:
        """Get book description from yaml or return a default one"""
        if 'description' in book and book['description']:
            return book['description']
        
        return f"A book about {book['field'].lower()}."

    def _generate_books_md(self, grouped_books):
        """Generate content for books.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Books"
author: "Mengxu"
date: {current_time}
lastmod: {current_time}
---

<!--more-->

Here is a curated list of ***Books*** covering various topics in bioinformatics, including single-cell RNA sequencing (scRNA-seq), genomics, and related fields. These resources are regularly updated and maintained.

"""
        content = []
        
        # Generate content for each field
        for field, books in grouped_books.items():
            # Add field as section header
            content.append(f"## {field}\n")
            content.append("| Title | Description |")
            content.append("| -- | -- |")
            
            # Add books in this field
            for book in books:
                description = self._get_description(book)
                content.append(f"| [{book['title']}]({book['url']}) | {description} |")
            
            content.append("\n")  # Add space between sections
        
        return header + '\n'.join(content)

    def _write_books_md(self, content):
        """Write content to books.md file"""
        with open(self.md_path, 'w', encoding='utf-8') as f:
            f.write(content) 