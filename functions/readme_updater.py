import os
from datetime import datetime
import logging
from typing import Dict, List
import yaml


class ReadmeUpdater:
    """Handler for updating both README.md and _index.md from various resource files"""

    def __init__(self, config_dir="config", content_dir="website/content"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.index_path = os.path.join(content_dir, "_index.md")
        self.readme_path = "README.md"
        self.logger = logging.getLogger(__name__)

    def update_readme(self):
        """Main method to update both README.md and _index.md files"""
        try:
            # Get latest entries from each category
            articles = self._get_latest_articles()
            methods = self._get_latest_methods()
            featured = {
                "blog": self._get_featured("blogs.yaml"),
                "book": self._get_featured("books.yaml"),
                "database": self._get_featured("databases.yaml"),
                "lab": self._get_featured("labs.yaml"),
            }

            # Generate content
            content = self._generate_index_md(articles, methods, featured)

            # Write to both files
            self._write_index_md(content)
            self._write_readme(content)

        except Exception as e:
            self.logger.error(f"Error updating readme files: {str(e)}")
            raise

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

    def _get_latest_articles(self) -> dict:
        """Get the latest article entry"""
        try:
            with open(
                os.path.join(self.config_dir, "articles.yaml"), "r", encoding="utf-8"
            ) as f:
                articles = yaml.safe_load(f)
                return sorted(articles, key=lambda x: x.get("date", ""), reverse=True)[
                    0
                ]
        except Exception:
            return {}

    def _get_latest_methods(self) -> dict:
        """Get the latest method entry"""
        try:
            with open(
                os.path.join(self.config_dir, "methods.yaml"), "r", encoding="utf-8"
            ) as f:
                methods = yaml.safe_load(f)
                return sorted(methods, key=lambda x: x.get("date", ""), reverse=True)[0]
        except Exception:
            return {}

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
        """Generate content for _index.md"""
        current_time = datetime.now().strftime("%Y-%m-%d")

        content = f"""# Bioinformatics Resources Collection

A comprehensive collection of bioinformatics resources, focusing on single-cell RNA sequencing (scRNA-seq) and related fields. This repository organizes resources into different categories for easy access and reference.

## 📚 Categories

### [Articles](posts/articles/index.html)
Research papers focusing on biological insights and discoveries using single-cell omics data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
| {latest_article.get('journal', '')} | {latest_article.get('date', '')} | [{latest_article.get('title', '')}]({latest_article.get('url', '')}) | {self._format_code_badge(latest_article)} | {self._format_data_badge(latest_article)} | {self._format_citation_badge(latest_article)} |

[View all articles →](posts/articles/index.html)

### [Methods](posts/methods/index.html)
Computational methods and tools for analyzing single-cell data.

**Latest Highlights:**
| Journal | Date | Title | Code | Data | Citation |
| -- | -- | -- | -- | -- | -- |
| {latest_method.get('journal', '')} | {latest_method.get('date', '')} | [{latest_method.get('title', '')}]({latest_method.get('url', '')}) | {self._format_code_badge(latest_method)} | {self._format_data_badge(latest_method)} | {self._format_citation_badge(latest_method)} |

[View all methods →](posts/methods/index.html)

### Learning Resources

#### [Blogs](posts/blogs/index.html)
Curated blog posts and articles about scRNA-seq and related topics.

**Featured Blog:**
| Field | Title |
| -- | -- |
| `{featured['blog'].get('field', '')}` | [{featured['blog'].get('title', '')}]({featured['blog'].get('url', '')}) |

[View all blogs →](posts/blogs/index.html)

#### [Books](posts/books/index.html)
Recommended books and learning materials.

**Featured Book:**
| Field | Title |
| -- | -- |
| `{featured['book'].get('field', '')}` | [{featured['book'].get('title', '')}]({featured['book'].get('url', '')}) |

[View all books →](posts/books/index.html)

#### [Databases](posts/databases/index.html)
Useful databases for bioinformatics research.

**Featured Database:**
| Field | Database | Description | Related paper |
| -- | -- | -- | -- |
| `{featured['database'].get('field', '')}` | [{featured['database'].get('title', '')}]({featured['database'].get('url', '')}) | {featured['database'].get('description', '')} | {self._format_paper_link(featured['database'])} |

[View all databases →](posts/databases/index.html)

#### [Labs](posts/labs/index.html)
Research laboratories and groups in the field.

**Featured Lab:**
| Field | Lab | Masterpiece |
| -- | -- | -- |
| `{featured['lab'].get('field', '')}` | [{featured['lab'].get('title', '')}]({featured['lab'].get('url', '')}) | [{featured['lab'].get('masterpiece', '')}]({featured['lab'].get('masterpiece_url', '')}) |

[View all labs →](posts/labs/index.html)

## 🤝 Contributing
Interested in contributing? We welcome contributions of all kinds:
1. Add new resources through pull requests
2. Report issues or suggest improvements
3. Help with documentation and examples

See [contribution guidelines](posts/description/index.html) for more details.

## 📝 Maintenance
For information about maintaining this project, please see:
- [Maintenance Guide](posts/description/index.html)
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
