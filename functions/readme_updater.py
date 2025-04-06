import os
from datetime import datetime
import logging
from typing import Dict, List, Optional
import yaml
import re


class ReadmeUpdater:
    def __init__(self):
        """Initialize readme updater"""
        self.logger = logging.getLogger(__name__)
        self.files = ["README.md", "website/content/_index.md"]
        self.max_items = 1  # Limit the number of items to display

    def _load_yaml(self, file_path):
        """Load yaml file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading {file_path}: {str(e)}")
            return None

    def format_data_links(self, data_list):
        """Format data links into readable format for README"""
        if not data_list:
            return ""

        formatted_links = []
        for data in data_list:
            if isinstance(data, dict):
                if "type" in data and "url" in data:
                    # Format as a badge with direct URL
                    data_type = data["type"]
                    data_url = data["url"]
                    formatted_links.append(
                        f"[![{data_type}](https://img.shields.io/badge/-{data_type}-c62764)]({data_url})"
                    )

        return "<br>".join(formatted_links) if formatted_links else ""

    def update_content(self):
        try:
            # Load all yaml files
            articles = self._load_yaml("config/articles.yaml")
            methods = self._load_yaml("config/methods.yaml")
            blogs = self._load_yaml("config/blogs.yaml")
            books = self._load_yaml("config/books.yaml")
            databases = self._load_yaml("config/databases.yaml")
            labs = self._load_yaml("config/labs.yaml")

            # Create content sections
            content = {}

            # Articles section
            if articles:
                if all("date" in article for article in articles):
                    articles.sort(key=lambda x: x["date"], reverse=True)
                recent_articles = articles[: self.max_items]
                content["articles"] = self._format_articles_table(recent_articles)

            # Methods section
            if methods:
                recent_methods = methods[: self.max_items]
                content["methods"] = self._format_methods_table(recent_methods)

            # Blogs section
            if blogs:
                recent_blogs = blogs[: self.max_items]
                content["blogs"] = self._format_blogs_table(recent_blogs)

            # Books section
            if books:
                recent_books = books[: self.max_items]
                content["books"] = self._format_books_table(recent_books)

            # Databases section
            if databases:
                recent_databases = databases[: self.max_items]
                content["databases"] = self._format_databases_table(recent_databases)

            # Labs section
            if labs:
                recent_labs = labs[: self.max_items]
                content["labs"] = self._format_labs_table(recent_labs)

            # Update all readme files
            success = True
            for file_path in self.files:
                try:
                    if not self._update_file(file_path, content):
                        self.logger.error(f"Failed to update {file_path}")
                        success = False
                    else:
                        self.logger.info(f"Successfully updated {file_path}")
                except Exception as e:
                    self.logger.error(f"Error updating {file_path}: {str(e)}")
                    success = False

            return success

        except Exception as e:
            self.logger.error(f"Error updating readme files: {str(e)}")
            self.logger.exception("Full traceback:")
            return False

    def _format_articles_table(self, articles):
        """Format articles into table"""
        table = [
            "**Latest Highlights:**\n",
            "| Journal | Date | Title | Code | Data | Citation |\n",
            "| -- | -- | -- | -- | -- | -- |\n",
        ]
        for article in articles:
            row = [
                article.get("journal", ""),
                article.get("date", ""),
                f"[{article['title']}]({article['url']})",
                f"[![R](https://img.shields.io/badge/-R-198ce7)]({article['code']})"
                if "code" in article
                else "",
                self.format_data_links(article.get("data", [])),
                f"[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F{article['citation']}%3Ffields%3DcitationCount)](https://api.semanticscholar.org/graph/v1/paper/{article['citation']})"
                if "citation" in article
                else "",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _format_methods_table(self, methods):
        """Format methods into table"""
        table = [
            "**Latest Highlights:**\n",
            "| Journal | Date | Title | Code | Data | Citation |\n",
            "| -- | -- | -- | -- | -- | -- |\n",
        ]
        for method in methods:
            row = [
                method.get("journal", ""),
                method.get("date", ""),
                f"[{method['title']}]({method['url']})",
                f"[![R](https://img.shields.io/badge/-R-198ce7)]({method['code']})"
                if "code" in method
                else "",
                self.format_data_links(method.get("data", [])),
                f"[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F{method['citation']}%3Ffields%3DcitationCount)](https://api.semanticscholar.org/graph/v1/paper/{method['citation']})"
                if "citation" in method
                else "",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _format_blogs_table(self, blogs):
        """Format blogs into table"""
        table = ["**Featured Blog:**\n", "| Field | Title |\n", "| -- | -- |\n"]
        for blog in blogs:
            row = [
                f"`{blog.get('field', '')}`",
                f"[{blog.get('title', '')}]({blog.get('url', '')})",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _format_books_table(self, books):
        """Format books into table"""
        table = ["**Featured Book:**\n", "| Field | Title |\n", "| -- | -- |\n"]
        for book in books:
            row = [
                f"`{book.get('field', '')}`",
                f"[{book.get('title', '')}]({book.get('url', '')})",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _format_databases_table(self, databases):
        """Format databases into table"""
        table = [
            "**Featured Database:**\n",
            "| Field | Database | Description | Related paper |\n",
            "| -- | -- | -- | -- |\n",
        ]
        for db in databases:
            row = [
                f"`{db.get('field', '')}`",
                f"[{db.get('title', '')}]({db.get('url', '')})",
                db.get("description", ""),
                f"[paper]({db.get('paper', '')})" if "paper" in db else "",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _format_labs_table(self, labs):
        """Format labs into table"""
        table = [
            "**Featured Lab:**\n",
            "| Field | Lab | Masterpiece |\n",
            "| -- | -- | -- |\n",
        ]
        for lab in labs:
            row = [
                f"`{lab.get('field', '')}`",
                f"[{lab.get('title', '')}]({lab.get('url', '')})",
                f"[{lab.get('masterpiece_name', '')}]({lab.get('masterpiece_url', '')})",
            ]
            table.append(f"| {' | '.join(row)} |\n")
        return table

    def _clean_content(self, content_list):
        """Clean content by removing duplicate headers and empty tables"""
        if not content_list:
            return []

        # Join all content into a single string
        content = "".join(content_list)

        # Remove duplicate headers and tables
        content = re.sub(
            r"(\*\*(?:Latest Highlights|Featured \w+):\*\*\n\|[^\n]*\n\|[^\n]*\n)+",
            "",
            content,
        )

        # Remove empty tables
        content = re.sub(r"\| [^\n]+ \|\n\| [-\s|]+ \|\n(?!\|)", "", content)

        return [content] if content.strip() else []

    def _update_file(self, file_path, content):
        """Update single readme file"""
        try:
            # Create the basic structure
            new_text = f"""# Bioinformatics Resources Collection

A comprehensive collection of bioinformatics resources, focusing on single-cell RNA sequencing (scRNA-seq) and related fields. This repository organizes resources into different categories for easy access and reference.

## 📚 Categories

"""
            # Articles section
            if "articles" in content and content["articles"]:
                new_text += """### [Articles](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/articles/index.html)
Research papers focusing on biological insights and discoveries using single-cell omics data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
"""
                new_text += "".join(self._clean_content(content["articles"]))
                new_text += "\n[View all articles →](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/articles/index.html)\n\n"

            # Methods section
            if "methods" in content and content["methods"]:
                new_text += """### [Methods](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/methods/index.html)
Computational methods and tools for analyzing single-cell data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
"""
                new_text += "".join(self._clean_content(content["methods"]))
                new_text += "\n[View all methods →](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/methods/index.html)\n\n"

            new_text += "### Learning Resources\n\n"

            # Learning resources sections
            sections = {
                "blogs": (
                    "Blogs",
                    "Curated blog posts and articles about scRNA-seq and related topics.",
                    "| Field | Title |\n| -- | -- |\n",
                ),
                "books": (
                    "Books",
                    "Recommended books and learning materials.",
                    "| Field | Title |\n| -- | -- |\n",
                ),
                "databases": (
                    "Databases",
                    "Useful databases for bioinformatics research.",
                    "| Field | Database | Description | Related paper |\n| -- | -- | -- | -- |\n",
                ),
                "labs": (
                    "Labs",
                    "Research laboratories and groups in the field.",
                    "| Field | Lab | Masterpiece |\n| -- | -- | -- |\n",
                ),
            }

            for section, (title, desc, table_header) in sections.items():
                if section in content and content[section]:
                    new_text += f"""#### [{title}](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/blogs/index.html)
{desc}

{table_header}"""
                    new_text += "".join(self._clean_content(content[section]))
                    new_text += f"\n[View all {section} →](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/{section}/index.html)\n\n"

            # Add remaining sections
            new_text += f"""## 🤝 Contributing
Interested in contributing? We welcome contributions of all kinds:
1. Add new resources through pull requests
2. Report issues or suggest improvements
3. Help with documentation and examples

See [contribution guidelines](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/description/index.html) for more details.

## 📝 Maintenance
For information about maintaining this project, please see:
- [Maintenance Guide](https://mengxu98.github.io/Bioinformatics_resources_collection/posts/description/index.html)
- [S2-folks Reference](https://github.com/allenai/s2-folks/tree/main)

*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""

            # Write the new content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_text)

            self.logger.info(f"Successfully updated {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating {file_path}: {str(e)}")
            self.logger.error(f"Full traceback:", exc_info=True)
            return False
