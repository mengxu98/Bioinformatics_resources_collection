import os
from datetime import datetime
import logging
from typing import Dict, List, Optional
import yaml
import re


class ReadmeUpdater:
    """Handler for updating both README.md and _index.md from various resource files"""

    def __init__(self, config_dir="config", content_dir="website/content"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.index_path = os.path.join(content_dir, "_index.md")
        self.readme_path = "README.md"
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.current_file = "README.md"

    def update_readme(self):
        """Update both README.md and _index.md with latest entries"""
        try:
            # Get first valid entries
            articles_path = os.path.join(self.content_dir, "posts", "articles.md")
            methods_path = os.path.join(self.content_dir, "posts", "methods.md")
            
            self.logger.info("Getting entries from articles and methods files...")
            article_entry = self._get_first_valid_entry(articles_path)
            method_entry = self._get_first_valid_entry(methods_path)
            
            self.logger.info(f"Article entry: {article_entry[:100]}...")
            self.logger.info(f"Method entry: {method_entry[:100]}...")
            
            # Update both files
            for file_path in ["README.md", os.path.join(self.content_dir, "_index.md")]:
                if not os.path.exists(file_path):
                    self.logger.warning(f"File not found: {file_path}")
                    continue
                    
                self.logger.info(f"Updating file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update articles section
                articles_table_start = content.find("**Latest Highlights:**\n| Journal")
                articles_table_end = content.find("[View all articles")
                
                self.logger.info(f"Articles section positions: {articles_table_start} to {articles_table_end}")
                
                if articles_table_start != -1 and articles_table_end != -1:
                    new_section = f"""**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
{article_entry}

"""
                    content = content[:articles_table_start] + new_section + content[articles_table_end-1:]
                
                # Update methods section
                methods_table_start = content.find("**Latest Highlights:**\n| Journal", content.find("### [Methods]"))
                methods_table_end = content.find("[View all methods")
                
                self.logger.info(f"Methods section positions: {methods_table_start} to {methods_table_end}")
                
                if methods_table_start != -1 and methods_table_end != -1:
                    new_section = f"""**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
{method_entry}

"""
                    content = content[:methods_table_start] + new_section + content[methods_table_end-1:]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"{os.path.basename(file_path)} updated successfully")
                
        except Exception as e:
            self.logger.error(f"Error updating readme files: {str(e)}")
            raise

    def _get_first_valid_entry(self, file_path):
        """Get the first valid entry from a markdown file"""
        try:
            self.logger.info(f"Reading file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            self.logger.info(f"Total lines in file: {len(lines)}")
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Skip empty lines and headers
                if not line or '---' in line or '<!--more-->' in line:
                    continue
                    
                # Skip table headers and category headers
                if '**Journal**' in line or '| --' in line or '**`' in line:
                    continue
                    
                # Must be a table row
                if not line.startswith('|') or not line.endswith('|'):
                    continue
                    
                # Split and clean parts
                parts = [p.strip() for p in line.split('|')]
                parts = [p for p in parts if p]  # Remove empty parts
                
                # Must have at least journal, date, and title
                if len(parts) < 3:
                    continue
                    
                journal = parts[0]
                date = parts[1]
                title = parts[2]
                
                # Skip if any required field is empty
                if not journal or not date or not title:
                    continue
                    
                # Skip category headers
                if '**`' in journal:
                    continue
                    
                # Must have a markdown link in title
                if '[' not in title or ']' not in title or '(' not in title or ')' not in title:
                    continue
                    
                self.logger.info(f"Found valid entry at line {i+1}:")
                self.logger.info(f"Journal: {journal}")
                self.logger.info(f"Date: {date}")
                self.logger.info(f"Title: {title}")
                
                return line
                
            self.logger.warning(f"No valid entries found in {file_path}")
            return '| N/A | N/A | [No entry available](#) |  |  |  |'
            
        except Exception as e:
            self.logger.error(f"Error reading entry from {file_path}: {str(e)}")
            return '| N/A | N/A | [No entry available](#) |  |  |  |'

    def _write_readme(self, content: str):
        """Write content to README.md file"""
        try:
            with open(self.readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.logger.info("README.md updated successfully")
        except Exception as e:
            self.logger.error(f"Error writing README.md: {str(e)}")
            raise

    def _write_index_md(self, content: str):
        """Write content to _index.md file"""
        try:
            with open(self.index_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.logger.info("_index.md updated successfully")
        except Exception as e:
            self.logger.error(f"Error writing _index.md: {str(e)}")
            raise

    def _parse_table_row(self, line: str) -> Optional[dict]:
        """Parse a single table row and return entry dict if valid"""
        try:
            # Split the line by | and clean up each part
            parts = [p.strip() for p in line.split('|')]
            
            # Skip invalid lines
            if len(parts) < 7:
                return None
            if not parts[1] or not parts[2] or not parts[3]:  # Check required fields
                return None
            if 'N/A' in parts[1] or '--' in parts[1] or '**`' in parts[1]:
                return None
            
            # Extract title and url from markdown link format
            title_part = parts[3]
            title = ""
            url = ""
            if '[' in title_part and ']' in title_part and '(' in title_part and ')' in title_part:
                title = title_part[title_part.find('[')+1:title_part.find(']')]
                url = title_part[title_part.find('(')+1:title_part.find(')')]
            else:
                return None
            
            return {
                'journal': parts[1],
                'date': parts[2],
                'title': title,
                'url': url,
                'code': parts[4] if len(parts) > 4 else '',
                'data': parts[5] if len(parts) > 5 else '',
                'citation': parts[6] if len(parts) > 6 else ''
            }
        except Exception as e:
            self.logger.debug(f"Error parsing row: {line}, error: {str(e)}")
            return None

    def _get_latest_methods(self) -> dict:
        """Get the latest method directly from methods.md"""
        try:
            # Check multiple possible paths
            possible_paths = [
                os.path.join(self.content_dir, "posts", "methods.md"),
                os.path.join(self.content_dir, "posts", "methods", "index.md")
            ]
            
            methods_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    methods_path = path
                    self.logger.info(f"Found methods at: {path}")
                    break
                
            if not methods_path:
                self.logger.warning("methods.md not found in any expected location")
                return self._get_empty_entry()

            with open(methods_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            latest_entry = None
            latest_date = None

            for line in content:
                # Skip headers, empty lines, and category lines
                if not line.strip() or '**Journal**' in line or '--' in line or '**`' in line:
                    continue
                
                # Skip lines that don't contain proper data
                if '|' not in line or line.count('|') < 5:
                    continue
                    
                entry = self._parse_table_row(line)
                if entry and entry['title'] != 'No entry available':
                    if not latest_date or entry['date'] > latest_date:
                        latest_date = entry['date']
                        latest_entry = entry

            return latest_entry if latest_entry else self._get_empty_entry()

        except Exception as e:
            self.logger.error(f"Error getting latest method: {str(e)}")
            return self._get_empty_entry()

    def _get_latest_articles(self) -> dict:
        """Get the latest article directly from articles.md"""
        try:
            articles_path = os.path.join(self.content_dir, "posts", "articles.md")
            self.logger.info(f"Found articles at: {articles_path}")
            
            with open(articles_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            latest_entry = None
            latest_date = None

            for line in content:
                # Skip headers, empty lines, and category lines
                if not line.strip() or '**Journal**' in line or '--' in line or '**`' in line:
                    continue
                
                # Skip lines that don't contain proper data
                if '|' not in line or line.count('|') < 5:
                    continue
                    
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 7 or not parts[1] or not parts[2]:
                    continue
                    
                # Skip category headers and empty entries
                if '**`' in parts[1] or not parts[3]:
                    continue
                    
                date = parts[2]
                if date and (not latest_date or date > latest_date):
                    latest_date = date
                    latest_entry = {
                        'journal': parts[1],
                        'date': date,
                        'title': parts[3].split(']')[0].replace('[', ''),
                        'url': parts[3].split('(')[1].split(')')[0],
                        'code': parts[4],
                        'data': parts[5],
                        'citation': parts[6]
                    }

            return latest_entry if latest_entry else self._get_empty_entry()

        except Exception as e:
            self.logger.error(f"Error getting latest article: {str(e)}")
            return self._get_empty_entry()

    def _get_empty_entry(self) -> dict:
        """Return an empty entry with default values"""
        return {
            'journal': 'N/A',
            'date': 'N/A',
            'title': 'No entry available',
            'url': '#',
            'code': '',
            'data': '',
            'citation': ''
        }

    def _get_featured(self, yaml_file: str) -> dict:
        """Get a featured entry from specified yaml file"""
        try:
            with open(
                os.path.join(self.config_dir, yaml_file), "r", encoding="utf-8"
            ) as f:
                entries = yaml.safe_load(f)
                # You might want to add a 'featured: true' field in yaml files
                # For now, just return the first entry
                return entries[0] if entries else {}
        except Exception:
            return {}

    def _generate_index_md(
        self, latest_article: dict, latest_method: dict, featured: Dict[str, dict]
    ) -> str:
        """Generate content for _index.md and README.md"""
        current_time = datetime.now().strftime("%Y-%m-%d")
        
        # Different link formats for README.md and _index.md
        is_readme = self.current_file == "README.md"
        base_url = "https://mengxu98.github.io/Bioinformatics_resources_collection" if is_readme else ""
        
        def get_link(path: str) -> str:
            """Get correct link format based on file type"""
            if is_readme:
                return f"{base_url}/{path}"
            return path

        content = f"""# Bioinformatics Resources Collection

A comprehensive collection of bioinformatics resources, focusing on single-cell RNA sequencing (scRNA-seq) and related fields. This repository organizes resources into different categories for easy access and reference.

## 📚 Categories

### [Articles]({get_link('posts/articles/index.html')})
Research papers focusing on biological insights and discoveries using single-cell omics data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
| {latest_article.get('journal', '')} | {latest_article.get('date', '')} | [{latest_article.get('title', '')}]({latest_article.get('url', '')}) | {latest_article.get('code', '')} | {latest_article.get('data', '')} | {latest_article.get('citation', '')} |

[View all articles →]({get_link('posts/articles/index.html')})

### [Methods]({get_link('posts/methods/index.html')})
Computational methods and tools for analyzing single-cell data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
| {latest_method.get('journal', '')} | {latest_method.get('date', '')} | [{latest_method.get('title', '')}]({latest_method.get('url', '')}) | {latest_method.get('code', '')} | {latest_method.get('data', '')} | {latest_method.get('citation', '')} |

[View all methods →]({get_link('posts/methods/index.html')})

### Learning Resources

#### [Blogs]({get_link('posts/blogs/index.html')})
Curated blog posts and articles about scRNA-seq and related topics.

**Featured Blog:**
| Field | Title |
| -- | -- |
| `{featured['blog'].get('field', '')}` | [{featured['blog'].get('title', '')}]({featured['blog'].get('url', '')}) |

[View all blogs →]({get_link('posts/blogs/index.html')})

#### [Books]({get_link('posts/books/index.html')})
Recommended books and learning materials.

**Featured Book:**
| Field | Title |
| -- | -- |
| `{featured['book'].get('field', '')}` | [{featured['book'].get('title', '')}]({featured['book'].get('url', '')}) |

[View all books →]({get_link('posts/books/index.html')})

#### [Databases]({get_link('posts/databases/index.html')})
Useful databases for bioinformatics research.

**Featured Database:**
| Field | Database | Description | Related paper |
| -- | -- | -- | -- |
| `{featured['database'].get('field', '')}` | [{featured['database'].get('title', '')}]({featured['database'].get('url', '')}) | {featured['database'].get('description', '')} | {self._format_paper_link(featured['database'])} |

[View all databases →]({get_link('posts/databases/index.html')})

#### [Labs]({get_link('posts/labs/index.html')})
Research laboratories and groups in the field.

**Featured Lab:**
| Field | Lab | Masterpiece |
| -- | -- | -- |
| `{featured['lab'].get('field', '')}` | [{featured['lab'].get('title', '')}]({featured['lab'].get('url', '')}) | [{featured['lab'].get('masterpiece', '')}]({featured['lab'].get('masterpiece_url', '')}) |

[View all labs →]({get_link('posts/labs/index.html')})

## 🤝 Contributing
Interested in contributing? We welcome contributions of all kinds:
1. Add new resources through pull requests
2. Report issues or suggest improvements
3. Help with documentation and examples

See [contribution guidelines]({get_link('posts/description/index.html')}) for more details.

## 📝 Maintenance
For information about maintaining this project, please see:
- [Maintenance Guide]({get_link('posts/description/index.html')})
- [S2-folks Reference](https://github.com/allenai/s2-folks/tree/main)

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments
Special thanks to all contributors and the bioinformatics community for their valuable resources and support.

*Last updated: {current_time}*
"""
        return content

    def _format_code_badge(self, entry: dict) -> str:
        """Format code badge based on programming language"""
        if "code_url" not in entry:
            return ""
        lang = entry.get("language", "Code")
        color = {"Python": "3572a5", "R": "198ce7"}.get(lang, "444444")
        return f'[![{lang}](https://img.shields.io/badge/-{lang}-{color})]({entry["code_url"]})'

    def _format_data_badge(self, entry: dict) -> str:
        """Format data badge"""
        badges = []
        if "geo_url" in entry:
            badges.append(
                f'[![GEO](https://img.shields.io/badge/-GEO-336699)]({entry["geo_url"]})'
            )
        if "zenodo_url" in entry:
            badges.append(
                f'[![Zenodo](https://img.shields.io/badge/-Zenodo-024dad)]({entry["zenodo_url"]})'
            )
        return " ".join(badges)

    def _format_citation_badge(self, entry: dict) -> str:
        """Format citation badge"""
        if "citation_url" not in entry:
            return ""
        return f'[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url={entry["citation_url"]})]({entry["citation_url"]})'

    def _format_paper_link(self, entry: dict) -> str:
        """Format paper link"""
        if "paper_url" not in entry:
            return ""
        return f'[paper]({entry["paper_url"]})'

    def _update_readme_content(self, content, articles_entry, methods_entry):
        """Update README.md content with latest entries"""
        # Update Articles section
        articles_start = content.find("**Latest Highlights:**\n| Journal")
        if articles_start != -1:
            table_end = content.find("\n\n[View all articles", articles_start)
            if table_end != -1:
                old_table = content[articles_start:table_end]
                new_table = f"""**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
{articles_entry}"""
                content = content.replace(old_table, new_table)

        # Update Methods section
        methods_start = content.find("**Latest Highlights:**\n| Journal", content.find("### [Methods]"))
        if methods_start != -1:
            table_end = content.find("\n\n[View all methods", methods_start)
            if table_end != -1:
                old_table = content[methods_start:table_end]
                new_table = f"""**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
{methods_entry}"""
                content = content.replace(old_table, new_table)

        return content

    def _format_entry_for_readme(self, entry: dict) -> str:
        """Format an entry for readme display"""
        if not entry or entry.get('title') == 'No entry available':
            return '| N/A | N/A | [No entry available](#) |  |  |  |'
        
        # Extract the first code badge if there are multiple
        code_badges = entry.get('code', '').split('[![')
        first_code = f"[![{code_badges[1]}" if len(code_badges) > 1 else ''
        
        # Extract the first data badge if there are multiple
        data_badges = entry.get('data', '').split('[![')
        first_data = f"[![{data_badges[1]}" if len(data_badges) > 1 else ''
        
        # Extract the citation badge
        citation_badge = entry.get('citation', '')
        
        return f"| {entry['journal']} | {entry['date']} | [{entry['title']}]({entry['url']}) | {first_code} | {first_data} | {citation_badge} |"
