import os
import logging
import yaml
from datetime import datetime
from itertools import groupby
from .extract_information import extract_paper_infor
import urllib.parse
from .badge_formatter import BadgeFormatter

class ArticlesUpdater:
    """Handler for updating articles.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "articles.yaml")
        self.md_path = os.path.join(content_dir, "articles.md")
        self.logger = logging.getLogger(__name__)

    def update_articles(self):
        """Main method to update articles.md file"""
        try:
            # Read existing articles
            articles_data = self._read_articles_yaml()
            
            # Complete missing information
            for article in articles_data:
                if self._needs_info_update(article):
                    self._complete_article_info(article)
            
            # Update yaml with completed information
            self._write_articles_yaml(articles_data)
            
            # Generate markdown
            grouped_articles = self._group_articles_by_field(articles_data)
            md_content = self._generate_articles_md(grouped_articles)
            self._write_articles_md(md_content)
            
        except Exception as e:
            self.logger.error(f"Error updating articles: {str(e)}")
            raise

    def _generate_articles_md(self, grouped_articles):
        """Generate content for articles.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Articles"
author: "Mengxu"
date: {current_time}
---
<!--more-->
| **Journal** | **Date** | **Title** | **Code** | **Data** | **Citation** |
| -- | -- | -- | -- | -- | -- |"""
        
        content = [header]
        
        for field, articles in grouped_articles.items():
            content.append(f"| **`{field}`** |  |  |  |  |  |")
            
            for article in articles:
                # Format all badges using BadgeFormatter
                code_badges = BadgeFormatter.format_code_badges(article)
                data_badges = BadgeFormatter.format_data_badges(article.get('data'))
                citation_badge = BadgeFormatter.format_citation_badge(article.get('citation'))
                
                row = (f"| {article['journal']} | {article['date']} | "
                      f"[{article['title']}]({article['url']}) | "
                      f"{code_badges} | {data_badges} | {citation_badge} |")
                
                content.append(row)
        
        return '\n'.join(content)

    def _read_articles_yaml(self):
        """Read articles from yaml file"""
        try:
            if os.path.exists(self.yaml_path):
                with open(self.yaml_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or []
            return []
        except Exception as e:
            self.logger.error(f"Error reading articles yaml: {str(e)}")
            return []

    def _group_articles_by_field(self, articles):
        """Group articles by their field"""
        if not articles:
            return {}
        sorted_articles = sorted(articles, key=lambda x: (x['field'].lower(), x['date'], x['title']))
        return {k: list(g) for k, g in groupby(sorted_articles, key=lambda x: x['field'])}

    def _write_articles_md(self, content):
        """Write content to articles.md file"""
        try:
            os.makedirs(os.path.dirname(self.md_path), exist_ok=True)
            with open(self.md_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.logger.error(f"Error writing articles md: {str(e)}")
            raise

    def _write_articles_yaml(self, articles_data):
        """Write updated articles back to yaml"""
        try:
            os.makedirs(os.path.dirname(self.yaml_path), exist_ok=True)
            with open(self.yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(articles_data, f, default_flow_style=False)
        except Exception as e:
            self.logger.error(f"Error writing articles yaml: {str(e)}")

    def _needs_info_update(self, article):
        """Check if article needs information update"""
        required_fields = ['journal', 'date', 'title', 'url']
        optional_fields = ['code', 'language', 'data', 'citation']
        
        # Check if any required field is missing
        if not all(field in article and article[field] for field in required_fields):
            return True
        
        # Check if any optional field that should be available is missing
        if article.get('code') and not article.get('language'):
            return True
        
        return False

    def _complete_article_info(self, article):
        """Complete missing information for an article"""
        try:
            if not article.get('url'):
                self.logger.warning(f"No URL provided for article: {article.get('title', 'Unknown')}")
                return

            # Create temporary file for extraction
            temp_file = "temp_article.md"
            extract_paper_infor(
                url_paper=article['url'],
                doi_paper=[''],
                code_language=article.get('code_language', []),
                url_code=[article.get('code', '')],
                data_database=[d.get('type', '') for d in article.get('data', [])] if isinstance(article.get('data'), list) else [],
                url_data=[d.get('url', '') for d in article.get('data', [])] if isinstance(article.get('data'), list) else [],
                file=temp_file
            )

            # Read and parse extracted information
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    content = f.read()
                os.remove(temp_file)
                
                # Update only missing information
                if not article.get('title'):
                    article['title'] = self._extract_between(content, "Title: ", "\n")
                if not article.get('date'):
                    article['date'] = self._extract_between(content, "Published date: ", "\n")
                if not article.get('journal'):
                    article['journal'] = self._extract_between(content, "Journal: ", "\n")
                
                # Handle code information
                if not article.get('code') or not article.get('language'):
                    code_info = self._extract_between(content, "The code provided by ", "...")
                    if code_info:
                        code_parts = code_info.split(", and from ")
                        if not article.get('language'):
                            article['language'] = code_parts[0] if len(code_parts) > 0 else ""
                        if not article.get('code'):
                            article['code'] = code_parts[1] if len(code_parts) > 1 else ""
                
                # Handle data information
                if not article.get('data'):
                    data_info = self._extract_between(content, "The dataset provided by ", "...")
                    if data_info:
                        data_parts = data_info.split(", and from ")
                        if len(data_parts) > 1:
                            article['data'] = [{
                                'type': data_parts[0],
                                'url': data_parts[1]
                            }]
                
        except Exception as e:
            self.logger.error(f"Error completing info for article {article.get('url')}: {str(e)}")

    def _extract_between(self, text, start, end):
        """Helper function to extract text between two markers"""
        try:
            s = text.index(start) + len(start)
            e = text.index(end, s)
            return text[s:e].strip()
        except:
            return ""